import os
import sqlite3
from datetime import date
from PySide import QtGui
from PySide import QtCore
from ui import ui_main

scripts_root = os.path.dirname(__file__).replace('\\', '/')


# Database
def init_database(sql_file_path):
    """
    Create database tables
    """

    connection = sqlite3.connect(sql_file_path)
    cursor = connection.cursor()

    # OLD
    # cursor.execute('''CREATE TABLE student (
    #                 id integer primary key autoincrement,
    #                 first_name text,
    #                 last_name text,
    #                 description text
    #                 )''')

    # User
    cursor.execute('''CREATE TABLE user (
                    id integer primary key autoincrement,
                    first_name text,
                    middle_name text,
                    last_name text,
                    email text,
                    address text,
                    phone text,
                    description text
                    )''')

    # Student application
    cursor.execute('''CREATE TABLE application (
                    id integer primary key autoincrement,
                    user_id integer,
                    date_received text,
                    status text,
                    transcripts text,
                    recommendations text,
                    gre_verbal text,
                    gre_quantitative text,
                    gre_analytical text,
                    experience text,
                    admission_term text,
                    degree_sought text,
                    prior1_major text,
                    prior1_year text,
                    prior1_gpa text,
                    prior1_university text,
                    prior2_major text,
                    prior2_year text,
                    prior2_gpa text,
                    prior2_university text,
                    description text,
                    FOREIGN KEY(user_id) REFERENCES user(id)
                    )''')

    connection.commit()
    connection.close()


class Student:
    def __init__(self, student_tuple):
        self.id = None
        self.first_name = ''
        self.last_name = ''
        self.description = ''

        self.init(student_tuple)

    def init(self, student_tuple):

        self.id = student_tuple[0]
        self.first_name = student_tuple[1]
        self.last_name = student_tuple[2]
        self.description = student_tuple[3]


class User:
    def __init__(self, user_tuple):
        self.id = None
        self.first_name = ''
        self.middle_name = ''
        self.last_name = ''
        self.email = ''
        self.address = ''
        self.phone = ''
        self.description = ''

        self.init(user_tuple)

    def init(self, user_tuple):

        self.id = user_tuple[0]
        self.first_name = user_tuple[1]
        self.middle_name = user_tuple[2]
        self.last_name = user_tuple[3]
        self.email = user_tuple[4]
        self.address = user_tuple[5]
        self.phone = user_tuple[6]
        self.description = user_tuple[7]


class Application:
    def __init__(self, application_tuple):
        self.id = None
        self.user_id = None
        self.date_received = ''
        self.status = ''
        self.transcripts = ''
        self.recommendations = ''
        self.gre_verbal = ''
        self.gre_quantitative = ''
        self.gre_analytical = ''
        self.experience = ''
        self.admission_term = ''
        self.degree_sought = ''
        self.prior1_major = ''
        self.prior1_year = ''
        self.prior1_gpa = ''
        self.prior1_university = ''
        self.prior2_major = ''
        self.prior2_year = ''
        self.prior2_gpa = ''
        self.prior2_university = ''
        self.description = ''

        self.init(application_tuple)

    def init(self, application_tuple):

        self.id = application_tuple[0]
        self.user_id = application_tuple[1]
        self.date_received = application_tuple[2]
        self.status = application_tuple[3]
        self.transcripts = application_tuple[4]
        self.recommendations = application_tuple[5]
        self.gre_verbal = application_tuple[6]
        self.gre_quantitative = application_tuple[7]
        self.gre_analytical = application_tuple[8]
        self.experience = application_tuple[9]
        self.admission_term = application_tuple[10]
        self.degree_sought = application_tuple[11]
        self.prior1_major = application_tuple[12]
        self.prior1_year = application_tuple[13]
        self.prior1_gpa = application_tuple[14]
        self.prior1_university = application_tuple[15]
        self.prior2_major = application_tuple[16]
        self.prior2_year = application_tuple[17]
        self.prior2_gpa = application_tuple[18]
        self.prior2_university = application_tuple[19]
        self.description = application_tuple[20]


# Data models
class AlignDelegate(QtGui.QItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = QtCore.Qt.AlignCenter
        QtGui.QItemDelegate.paint(self, painter, option, index)


class Students:
    def __init__(self, sql_file_path):
        self.sql_file_path = sql_file_path
        self.list_students = []

    def convert_to_students(self, student_tuples):

        students = []

        for student_tuple in student_tuples:
            student = Student(student_tuple)
            students.append(student)

        return students

    def add_student(self, student_tuple):

        # Create student object
        student = Student(student_tuple)

        connection = sqlite3.connect(self.sql_file_path)
        cursor = connection.cursor()

        # Add object to DB
        cursor.execute("INSERT INTO student VALUES ("
                       ":id,"
                       ":first_name,"
                       ":last_name,"
                       ":description)",

                       {'id': cursor.lastrowid,
                        'first_name': student.first_name,
                        'last_name': student.last_name,
                        'description': student.description})

        connection.commit()
        student.id = cursor.lastrowid  # Add database ID to the object
        connection.close()

        # Add student to data instance
        self.list_students.append(student)

    def get_students(self):

        connection = sqlite3.connect(self.sql_file_path)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student")
        student_tuples = cursor.fetchall()
        connection.close()

        if student_tuples:
            student_objects = self.convert_to_students(student_tuples)
            self.list_students.extend(student_objects)


class StudentsModel(QtCore.QAbstractTableModel):
    def __init__(self, students, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)

        self.students = students
        self.header = ['  Id  ', '  First Name ', '  Last Name ', '  Description  ']

    # Build-in functions
    def flags(self, index):

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]

    def rowCount(self, parent):

        if not self.students.list_students:
            return 0

        return len(self.students.list_students)

    def columnCount(self, parent):

        return len(self.header)

    def data(self, index, role):

        if not index.isValid():
            return

        row = index.row()
        column = index.column()
        student = self.students.list_students[row]

        if role == QtCore.Qt.DisplayRole:  # Fill table data to DISPLAY
            if column == 0:
                return student.id

            if column == 1:
                return student.first_name

            if column == 2:
                return student.last_name

            if column == 3:
                return student.description


class StarrsData:
    def __init__(self, sql_file_path):
        self.sql_file_path = sql_file_path

    # Tuple to object conversion
    def convert_to_application(self, application_tuples):

        applications = []

        for application_tuple in application_tuples:
            application = Application(application_tuple)
            applications.append(application)

        return applications

    def add_user(self, user_tuple):

        user = User(user_tuple)

        connection = sqlite3.connect(self.sql_file_path)
        cursor = connection.cursor()

        # Add object to DB
        cursor.execute("INSERT INTO user VALUES ("
                       ":id,"
                       ":first_name,"
                       ":middle_name,"
                       ":last_name,"
                       ":email,"
                       ":address,"
                       ":phone,"
                       ":description)",

                       {'id': cursor.lastrowid,
                        'first_name': user.first_name,
                        'middle_name': user.middle_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'address': user.address,
                        'phone': user.phone,
                        'description': user.description})

        connection.commit()
        user.id = cursor.lastrowid  # Add database ID to the object
        connection.close()

        print 'User {0} {1} added!'.format(user.first_name, user.last_name)
        return user

    def add_application(self, application_tuple):

        application = Application(application_tuple)

        connection = sqlite3.connect(self.sql_file_path)
        cursor = connection.cursor()

        # Add object to DB
        cursor.execute("INSERT INTO application VALUES ("
                       ":id,"
                       ":user_id,"
                       ":date_received,"
                       ":status,"
                       ":transcripts,"
                       ":recommendations,"
                       ":gre_verbal,"
                       ":gre_quantitative,"
                       ":gre_analytical,"
                       ":experience,"
                       ":admission_term,"
                       ":degree_sought,"
                       ":prior1_major,"
                       ":prior1_year,"
                       ":prior1_gpa,"
                       ":prior1_university," 
                       ":prior2_major,"
                       ":prior2_year,"
                       ":prior2_gpa,"
                       ":prior2_university,"
                       ":description)",

                       {'id': cursor.lastrowid,
                        'user_id': application.user_id,
                        'date_received': application.date_received,
                        'status': application.status,
                        'transcripts': application.transcripts,
                        'recommendations': application.recommendations,
                        'gre_verbal': application.gre_verbal,
                        'gre_quantitative': application.gre_quantitative,
                        'gre_analytical': application.gre_analytical,
                        'experience': application.experience,
                        'admission_term': application.admission_term,
                        'degree_sought': application.degree_sought,
                        'prior1_major': application.prior1_major,
                        'prior1_year': application.prior1_year,
                        'prior1_gpa': application.prior1_gpa,
                        'prior1_university': application.prior1_university,
                        'prior2_major': application.prior2_major,
                        'prior2_year': application.prior2_year,
                        'prior2_gpa': application.prior2_gpa,
                        'prior2_university': application.prior2_university,
                        'description': application.description})

        connection.commit()
        application.id = cursor.lastrowid  # Add database ID to the object
        connection.close()

        print 'Application for user {} added!'.format(application.user_id)

    def get_application(self, user_id):

        connection = sqlite3.connect(self.sql_file_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM application WHERE user_id=:user_id",
                       {'user_id': user_id})

        application_tuple = cursor.fetchone()

        connection.close()

        if application_tuple:
            return self.convert_to_application([application_tuple])[0]

    def add_student_data(self, user_id, transcripts, recommendations):
        """
        GS enters transcripts and recommendations
        """

        connection = sqlite3.connect(self.sql_file_path)
        cursor = connection.cursor()

        cursor.execute("UPDATE application SET "
                       "transcripts=:transcripts,"
                       "recommendations=:recommendations "

                       "WHERE user_id=:user_id",

                       {'user_id': user_id,
                        'transcripts': transcripts,
                        'recommendations': recommendations
                        })

        connection.commit()
        connection.close()

    def set_status(self, user_id, status):
        """
        Set applicant status
        """

        connection = sqlite3.connect(self.sql_file_path)
        cursor = connection.cursor()

        cursor.execute("UPDATE application SET "
                       "status=:status "

                       "WHERE user_id=:user_id",

                       {'user_id': user_id,
                        'status': status
                        })

        connection.commit()
        connection.close()


# STARRS Application
class STARRS(QtGui.QMainWindow, ui_main.Ui_STARRS):
    def __init__(self, parent=None):
        super(STARRS, self).__init__(parent=parent)

        # SETUP UI
        self.setupUi(self)
        # self.tabStudents.hide()

        # # Data
        # self.students_model = None
        # self.students_data = None
        #
        # # Load students
        # self.init_students()
        # self.btnAddStudent.clicked.connect(self.add_student)

        # Database
        self.sql_file_path = '{0}/data/database.db'.format(scripts_root)
        if not os.path.exists(self.sql_file_path):
            self.init_database()

        # Starrs data
        self.starrs_data = None

        # Init UI data
        self.init_ui()
        self.init_data()

        # UI functionality
        self.actInitDatabase.triggered.connect(self.init_database)

        self.btnSubmitApplication.pressed.connect(self.submit_application)
        self.btnCheckApplicationStatus.pressed.connect(self.check_application_status)

        self.btnAddStudentData.pressed.connect(self.add_student_data)
        self.btnMadeDecision.pressed.connect(self.set_status)

    def init_ui(self):

        # Temp fill forms
        # Application
        self.linStudentFirstName.setText('Kiryha')
        self.linStudentLastName.setText('Krysko')
        self.linGREVErbal.setText('170')
        self.linGREVQuant.setText('170')
        self.linGREVAnalitical.setText('6')
        self.linApplicantEmail.setText('coder@umich.edu')
        self.linApplicantPhone.setText('734-780-9383')
        self.linAddressZip.setText('48067')
        self.linAddressState.setText('MI')
        self.linAddressCity.setText('Royal Oak')
        self.linAddressStreet.setText('W 6th st')
        self.linWorkExpirience.setText('I was working as developer at Google. In my dreams.')
        self.linPriorDegree1.setText('Bachelor')
        self.linPriorYear1.setText('1998')
        self.linPriorGPA1.setText('3.2')
        self.linPriorUniversity1.setText('KTILP')
        self.linPriorDegree2.setText('Master')
        self.linPriorYear2.setText('1999')
        self.linPriorGPA2.setText('3.6')
        self.linPriorUniversity2.setText('KTILP')
        # Admission
        self.linTranscript.setText('Transcripts')
        self.linRecommendation.setText('Recommendations')

        self.comDegreeSought.addItems(['MS', 'MSE'])
        self.comAdmissionTerm.addItems(['S2022', 'F2022', 'W2023', 'S2023', 'F2023'])
        self.comDescision.addItems(['Admitted with Aid', 'Admitted', 'Rejected'])

    def init_data(self):

        self.starrs_data = StarrsData(self.sql_file_path)

    def get_ui_apply(self):

        user_tuple = [
            None,
            self.linStudentFirstName.text(),
            self.linStudentMidName.text(),
            self.linStudentLastName.text(),
            self.linApplicantEmail.text(),
            '{0}, {1}, {2}, {3}'.format(self.linAddressZip.text(),
                                        self.linAddressState.text(),
                                        self.linAddressCity.text(),
                                        self.linAddressStreet.text()),
            self.linApplicantPhone.text(),
            '']

        application_tuple = [
            None,  # id
            None,  # user_id
            date.today().strftime('%d/%m/%Y'),  # date received
            None,  # status
            None,  # transcripts
            None,  # recommendations
            self.linGREVErbal.text(),
            self.linGREVQuant.text(),
            self.linGREVAnalitical.text(),
            self.linWorkExpirience.text(),
            self.comAdmissionTerm.currentText(),
            self.comDegreeSought.currentText(),
            self.linPriorDegree1.text(),
            self.linPriorYear1.text(),
            self.linPriorGPA1.text(),
            self.linPriorUniversity1.text(),
            self.linPriorDegree2.text(),
            self.linPriorYear2.text(),
            self.linPriorGPA2.text(),
            self.linPriorUniversity2.text(),
            'description']

        return user_tuple, application_tuple

    def setup_table(self, table):

        table.verticalHeader().hide()
        table.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        table.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        table.horizontalHeader().setStretchLastSection(True)
        table.setItemDelegate(AlignDelegate())

    def init_students(self):

        self.setup_table(self.tabStudents)

        self.students_data = Students(self.sql_file_path)
        self.students_data.get_students()

        self.students_model = StudentsModel(self.students_data)
        self.tabStudents.setModel(self.students_model)

    def init_database(self):
        """
        Create empty database tables
        """

        init_database(self.sql_file_path)

    def add_student(self):

        first_name = self.linStudentFirstName.text()
        last_name = self.linStudentLastName.text()
        description = self.linStudentDescription.text()
        student_tuple = [None, first_name, last_name, description]

        self.students_model.layoutAboutToBeChanged.emit()
        self.students_data.add_student(student_tuple)
        self.students_model.layoutChanged.emit()

    # 1) Online Application
    def submit_application(self):

        # Add user
        user_tuple, application_tuple = self.get_ui_apply()
        user = self.starrs_data.add_user(user_tuple)

        # Sent password
        self.statusBar().showMessage('>> Password is: >{0}<'.format(user.id))

        # Add application
        application_tuple[1] = user.id
        self.starrs_data.add_application(application_tuple)

    def check_application_status(self):
        """
        The status is:
            Application Materials Missing
            Application Received and Decision Pending
            Admission Decision: Accepted
            Admission Decision: Rejected
        """

        # Get user application
        user_id = self.lineStudentID.text()
        application = self.starrs_data.get_application(user_id)

        if not application:
            self.labApplicationStatus.setText('Application status: Application Was Not Submitted!')
            return

        if application.status:
            self.labApplicationStatus.setText('Application status: Admission Decision: {}'.format(application.status))

        else:
            if application.transcripts and application.recommendations:
                self.labApplicationStatus.setText('Application status: Application Received and Decision Pending')
            else:
                missing = ''
                if not application.transcripts:
                    missing += 'transcripts'
                if not application.recommendations:
                    missing += ' and recommendations'

                self.labApplicationStatus.setText('Application status: Application Materials Missing: {}'.format(missing))

    # 2) Admission process
    def add_student_data(self):
        """
        Add transcripts and recommendations by GS
        """

        user_id = self.linStudentIDAdmission.text()
        transcripts = self.linTranscript.text()
        recommendations = self.linRecommendation.text()

        self.starrs_data.add_student_data(user_id, transcripts, recommendations)
        self.statusBar().showMessage('>> Applicant {0} data submitted!'.format(user_id))

    def set_status(self):
        """
        Admit/reject applicant by GS
        """

        user_id = self.linStudentIDAdmission.text()
        status = self.comDescision.currentText()

        self.starrs_data.set_status(user_id, status)


if __name__ == "__main__":
    app = QtGui.QApplication([])
    starrs = STARRS()
    starrs.show()
    app.exec_()
