//
//  runview.hpp
//  PyAircraft
//
//  Created by 田中伟 on 2017/5/4.
//  Copyright © 2017年 田中伟. All rights reserved.
//

#ifndef runview_hpp
#define runview_hpp

#include <QtWidgets>

struct RunOption
{
    QString Path;
    QString Program;
};

class RunView : public QDialog
{
    Q_OBJECT
    
public:
    RunView(RunOption *pOption, QWidget *parent=NULL);
    ~RunView();
    
public slots:
    void accept();
    
private:
    void initSettings();
    
    QLineEdit *programEdit, *pathEdit;
    
    QWidget *settingWidget;
    QTabWidget *tab;
    QPushButton *runBtn, *cancelBtn;
    
    RunOption *option;
};

#endif /* runview_hpp */
