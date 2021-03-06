# -*- coding: utf-8 -*- 
from   PySide.QtGui		               import *
from   PySide.QtCore		           import *
from   time                            import sleep
from   selenium                        import webdriver
from   selenium.webdriver.common.keys  import Keys
from   selenium.webdriver.common.alert import Alert
from   django.utils.encoding           import smart_str, smart_text
import sys
import pickle


		  
class MainWindow( QWidget ):
	def __init__( self, parent = None ):
		super( MainWindow, self ).__init__( parent )
		self.setGeometry( 900, 300, 420, 620 )
		self.setWindowTitle(u'Auto Login Bot')
		self.mainPageItemArray = []
		self.runList           = []
		self.driverList        = []
		self.Vbox	   = QVBoxLayout()
		self.Hbox_1	   = QHBoxLayout()
		self.Hbox_2	   = QHBoxLayout()
		self.urlText   = QLineEdit  ()		
		self.treeArea  = QTreeWidget()
		self.submit    = QPushButton( 'Open key file',                self )
		self.clear	   = QPushButton( 'Clear List',                   self )
		self.export	   = QPushButton( 'Run Script',                   self )
		self.loadImg   = QCheckBox  ( 'Load Image\n[     Slow     ]', self )

		self.loadImg.setChecked( True )
		self.submit.setMinimumHeight ( 30 )
		self.urlText.setMinimumHeight( 30 )
		self.treeArea.setColumnCount ( 3  )
		self.treeArea.header().resizeSection( 0, 130 )
		self.treeArea.header().resizeSection( 1,  65 )
		self.treeArea.header().resizeSection( 2, 180 )
		self.treeArea.setHeaderLabels( ['Name', 'User ID', 'User Password'] )
		self.treeArea.setSelectionMode( QAbstractItemView.MultiSelection )

		self.setLayout( self.Vbox )
		self.Hbox_1.addWidget( self.urlText )
		self.Hbox_1.addWidget( self.submit  )
		self.Hbox_2.addStretch()
		self.Hbox_2.addWidget( self.clear   )
		self.Hbox_2.addWidget( self.export  )
		self.Hbox_2.addWidget( self.loadImg )
		self.Hbox_2.addStretch()
		self.Vbox.addLayout( self.Hbox_1   )
		self.Vbox.addWidget( self.treeArea )
		self.Vbox.addLayout( self.Hbox_2   )
		
		self.submit.clicked.connect( self.loadKeyList       )
		self.clear.clicked.connect ( self.clearTree         )
		self.export.clicked.connect( self.setupLogWebThread )


	def loadKeyList( self ):
		filePath, _ = QFileDialog.getOpenFileName( self, 'Open file', './', filter ='*.key' )
		keyFile     = open( './list.key', 'r' )
		lines       = smart_text( keyFile.read() ).split( '\n' )
		self.urlText.setText(filePath) 
		keyFile.close()

		for line in lines:
			key = line.split( '\t' )
			if len( key ) == 3:
				self.addKey( key )	
				# print 'adding  [{0}--{1}--{2}]  to list.'.format( smart_str(key[2]), key[0], key[1] )
		for item in self.mainPageItemArray:
			item.setSelected( True )


	def addKey( self, key ):
		pageItem = QTreeWidgetItem()
		pageItem.setText( 0, key[2] )
		pageItem.setText( 1, key[0] )
		pageItem.setText( 2, key[1] )
		self.treeArea.addTopLevelItem( pageItem )
		self.mainPageItemArray.append( pageItem )



	def setupLogWebThread( self ):  
		self.runList = []
		for item in self.mainPageItemArray:
			if item.isSelected():
				self.runList.append( item )
				item.setSelected( False )

		self.logWebThread = logWeb( self.runList, self.loadImg.isChecked() )
		self.logWebThread.threadDone.connect (  self.doneThread,      Qt.DirectConnection )
		self.logWebThread.threadError.connect(  self.setErrorKey,     Qt.QueuedConnection )
		self.logWebThread.threadValid.connect(  self.setSuccessKey,   Qt.QueuedConnection )
		self.logWebThread.threadDriver.connect( self.driverCollector, Qt.QueuedConnection )

		if not self.logWebThread.isRunning():
			self.urlText.setDisabled( True )
			self.submit.setDisabled ( True )
			self.clear.setDisabled  ( True )
			self.export.setDisabled ( True )
			self.loadImg.setDisabled( True )
			self.submit.setText( 'Processing...' )
			self.logWebThread.start()
	

	def doneThread( self ):
		self.submit.setText( 'open key file' )
		self.urlText.setDisabled( False )
		self.submit.setDisabled ( False )
		self.clear.setDisabled  ( False )
		self.export.setDisabled ( False )
		self.loadImg.setDisabled( False )


	def driverCollector( self, driver ):
		self.driverList.append( driver )


	def setErrorKey( self, index ):
		errorItem = self.runList[index]
		errorItem.setText( 0, '[x]' + errorItem.data( 0, 0 ))
		errorItem.setBackground ( 0, QBrush( QColor( 180, 0, 0 )))
		errorItem.setBackground ( 1, QBrush( QColor( 180, 0, 0 )))
		errorItem.setBackground ( 2, QBrush( QColor( 180, 0, 0 )))


	def setSuccessKey( self, index ):
		validItem = self.runList[index]
		validItem.setBackground ( 0, QBrush( QColor( 0, 180, 0 )))
		validItem.setBackground ( 1, QBrush( QColor( 0, 180, 0 )))
		validItem.setBackground ( 2, QBrush( QColor( 0, 180, 0 )))
		

	def clearTree( self ):
		self.treeArea.clear()
		self.mainPageItemArray = []


	def exportTree( self ):
		for errorItem in self.mainPageItemArray:
			errorItem.setText( 0, errorItem.data( 0, 0 ) + ' --login faild.' )
			print errorItem.background( 0 )
			errorItem.setBackground ( 0, QBrush( QColor( 180, 0, 0 )))
			errorItem.setBackground ( 1, QBrush( QColor( 180, 0, 0 )))
			errorItem.setBackground ( 2, QBrush( QColor( 180, 0, 0 )))


	def closeEvent( self, event ):
		for driver in self.driverList:
			try:
				driver.quit()
			except:
				pass
		event.accept()




class logWeb( QThread ):
	threadDone	  = Signal()
	threadError   = Signal( int    )
	threadValid   = Signal( int    )
	threadDriver  = Signal( object )

	def __init__( self, keyList, loadImage, parent = None ):
		super(logWeb ,self).__init__(parent) 
		self.exiting     = False  
		self.keyList     = keyList
		self.loadImage   = loadImage
		self.driverList  = []


	def run( self ):
		if len( self.keyList ) != 0:  
			self.AqrData( self.keyList, self.loadImage )
		self.threadDone.emit()


	def AqrData( self, keyList, loadImage ):
		for index, key in enumerate( keyList ):
			userID = key.data( 1, 0 )
			userPW = key.data( 2, 0 )
			option = webdriver.ChromeOptions()

			if not loadImage:
				option = webdriver.ChromeOptions()
				prefs  = { "profile.managed_default_content_settings.images":2 }
				option.add_experimental_option( "prefs", prefs )

			driver = webdriver.Chrome( './chromedriver', chrome_options = option )
			self.threadDriver.emit( driver )	
			driver.get( "https://********/" )
			driver = self.handleCookies( driver, index )
			self.driverList.append( driver )

			assert u"教育部" in driver.title

			try:
				ID_elem = driver.find_element_by_name( "strUserID" )
				PW_elem = driver.find_element_by_name( "strPwd"    )
				ID_elem.send_keys( userID      )
				PW_elem.send_keys( userPW      )
				PW_elem.send_keys( Keys.RETURN )
				sleep( 1 )

				try:
					alert = driver.switch_to_alert()
					print   smart_str( alert.text ) 
					self.threadError.emit( index )
					driver.close()
				except:
					self.threadValid.emit( index )

			except:
				self.threadError.emit( index )	
		return 0


	def handleCookies( self, driver, index ):
		if index == 0:
			pickle.dump( driver.get_cookies() , open( "./cookies/main.pkl", "wb" ))

		else:
			cookies = pickle.load( open( "./cookies/main.pkl", "rb" ))
			for cookie in cookies:
				driver.add_cookie( cookie )

		return driver




if __name__ == '__main__':
	app     = QApplication( sys.argv )
	frame   = MainWindow()
	frame.show()	
	app.exec_()
	sys.exit