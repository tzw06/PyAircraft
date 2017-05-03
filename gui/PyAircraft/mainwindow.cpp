//
//  mainwindow.cpp
//  PyAircraft
//
//  Created by 田中伟 on 2017/4/30.
//  Copyright © 2017年 田中伟. All rights reserved.
//

#include "mainwindow.h"
#include "inspector.h"
#include <QtXml>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    createView();
    createActions();
    createToolbar();
    
    setUnifiedTitleAndToolBarOnMac(true);
    
    readSettings();
    
    proc = new QProcess(this);
    connect(proc, SIGNAL(readyReadStandardOutput()), this, SLOT(onReadOutput()));
}

MainWindow::~MainWindow()
{
    delete proc;
}

void MainWindow::closeEvent(QCloseEvent *event)
{
    writeSettings();
}

void MainWindow::open()
{
    QString filename = QFileDialog::getOpenFileName(this, "open project file", QDir::currentPath(), "XML files (*.xml)");
    if (filename=="")
        return;
    
    QString suffix = ".xml";
    if (!filename.endsWith(suffix))
        filename = filename + suffix;
    
    QFile file(QString::fromLocal8Bit(filename.toLocal8Bit()));
    if (!file.open(QFile::ReadOnly | QFile::Text)) {
        QMessageBox::warning(this, tr("Loading from file"),
                             QString(tr("Cannot read file %1:\n%2")).arg(filename).arg(file.errorString()));
        return;
    }
    
    QDomDocument doc;
    QDomElement rootElement;
    
    doc.setContent(&file);
    rootElement = doc.documentElement();
    
    inspector->setContent(rootElement);
    
    QDir::setCurrent(QFileInfo(filename).absolutePath());
}

void MainWindow::save()
{
    
}

void MainWindow::run()
{
    QString program = "/Users/tzw/SDK/PyAircraft/core/main.py";
    QStringList arguments;
    arguments << "outline" << "report";
    
    proc->start(program, arguments);
}

void MainWindow::onShowInspector(bool is)
{
    inspector->setVisible(is);
}

void MainWindow::onReadOutput()
{
    QByteArray ba = proc->readAllStandardOutput();
    edit->append(ba);
}

void MainWindow::createView()
{
    edit = new QTextEdit(this);
    
    inspector = new Inspector(this);
    
    QSplitter *splitter = new QSplitter(Qt::Horizontal, this);
    splitter->setHandleWidth(0);
    splitter->addWidget(edit);
    splitter->addWidget(inspector);
    splitter->setStretchFactor(0, 1);
    
    setCentralWidget(splitter);
}

void MainWindow::createActions()
{
    openAct = new QAction(QIcon(":images/open.png"), "Open", this);
    openAct->setShortcuts(QKeySequence::Open);
    connect(openAct, SIGNAL(triggered(bool)), this, SLOT(open()));

    saveAct = new QAction(QIcon(":images/save.png"), "Save", this);
    saveAct->setShortcuts(QKeySequence::Save);
    connect(saveAct, SIGNAL(triggered(bool)), this, SLOT(save()));
    
    runAct = new QAction(QIcon(":images/play.png"), "Run", this);
    runAct->setShortcut(QKeySequence(Qt::CTRL+Qt::Key_R));
    connect(runAct, SIGNAL(triggered(bool)), this, SLOT(run()));
    
    inspectorAct = new QAction(QIcon(":images/property.png"), "Inspector", this);
    inspectorAct->setCheckable(true);
    inspectorAct->setChecked(true);
    connect(inspectorAct, SIGNAL(triggered(bool)), this, SLOT(onShowInspector(bool)));
}

void MainWindow::createToolbar()
{
    QToolBar *bar = addToolBar("toolBar");
    bar->setObjectName("toolBar");
    bar->setIconSize(QSize(24,24));
    bar->setMovable(false);
    bar->setFloatable(false);
    
    QWidget *spacer = new QWidget(this);
    spacer->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
    
    bar->addAction(openAct);
    bar->addAction(saveAct);
    bar->addWidget(spacer);
    bar->addAction(runAct);
    bar->addAction(inspectorAct);
}

void MainWindow::readSettings()
{
    QSettings settings("COMAC", "PyAircraft");
    
    QDir::setCurrent(settings.value("current-path", "").toString());
    
    //  Window Geometry
    restoreGeometry(settings.value("geometry").toByteArray());
    restoreState(settings.value("state").toByteArray());
    
    move(settings.value("pos", QPoint(200,200)).toPoint());
    resize(settings.value("size", QSize(800,600)).toSize());
    
    QString winstate = settings.value("window-state", "normal").toString();
    if (winstate=="maximized")
        showMaximized();
    else
        showNormal();
}

void MainWindow::writeSettings()
{
    QSettings settings("COMAC", "PyAircraft");
    
    //  Window Geometry
    if ( (!isMaximized()) && (!isMinimized()) ) {
        settings.setValue("pos", pos());
        settings.setValue("size", size());
    }
    if (isMaximized())
        settings.setValue("window-state", "maximized");
    else
        settings.setValue("window-state", "normal");
    settings.setValue("state", saveState());
    
    settings.setValue("current-path", QDir::currentPath());
    
}
