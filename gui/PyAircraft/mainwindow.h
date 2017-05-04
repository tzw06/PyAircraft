//
//  mainwindow.hpp
//  PyAircraft
//
//  Created by 田中伟 on 2017/4/30.
//  Copyright © 2017年 田中伟. All rights reserved.
//

#ifndef mainwindow_hpp
#define mainwindow_hpp

#include <QtWidgets>

class RunOption;
class Inspector;

class MainWindow : public QMainWindow
{
    Q_OBJECT
    
public:
    MainWindow(QWidget *parent=NULL);
    ~MainWindow();
 
    void closeEvent(QCloseEvent *event);
    
private slots:
    void open();
    void save();
    void run();
    void onShowInspector(bool is);
    void onReadOutput();
    void onRunFinished(int,QProcess::ExitStatus);
    
private:
    void createView();
    void createActions();
    void createToolbar();
    
    void readSettings();
    void writeSettings();
    
    void loadFromFile(QString filename);
    void updateFromFile(QString filename);
    void saveToFile(QString filename);
    
    QAction *openAct, *saveAct;
    QAction *inspectorAct, *runAct;
    
    QTextEdit *edit;
    Inspector *inspector;
    
    QProcess *proc;
    RunOption *option;
};


#endif /* mainwindow_hpp */
