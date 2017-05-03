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
    
private:
    void createView();
    void createActions();
    void createToolbar();
    
    void readSettings();
    void writeSettings();
    
    QAction *openAct, *saveAct;
    QAction *inspectorAct, *runAct;
    
    QTextEdit *edit;
    Inspector *inspector;
    
    QProcess *proc;
};


#endif /* mainwindow_hpp */
