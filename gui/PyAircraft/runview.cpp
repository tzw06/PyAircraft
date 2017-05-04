//
//  runview.cpp
//  PyAircraft
//
//  Created by 田中伟 on 2017/5/4.
//  Copyright © 2017年 田中伟. All rights reserved.
//

#include "runview.h"

RunView::RunView(RunOption *pOption, QWidget *parent)
    : QDialog(parent)
{
    option = pOption;
    setWindowFlags(Qt::Sheet);
    
    initSettings();

    runBtn = new QPushButton(tr("Run"), this);
    cancelBtn = new QPushButton(tr("Cancel"), this);
    
    QGridLayout *layout = new QGridLayout;
    layout->addWidget(tab, 0,0,1,3);
    layout->addWidget(cancelBtn, 1,1);
    layout->addWidget(runBtn, 1,2);
    
    setLayout(layout);
    
    connect(runBtn, SIGNAL(clicked()), this, SLOT(accept()));
    connect(cancelBtn, SIGNAL(clicked()), this, SLOT(close()));
    
}

RunView::~RunView()
{
    
}

void RunView::accept()
{
    option->Program = programEdit->text();
    option->Path = pathEdit->text();
    
    QDialog::accept();
}

void RunView::initSettings()
{
    programEdit = new QLineEdit(option->Program, this);
    pathEdit = new QLineEdit(option->Path, this);
    
    QFormLayout *settingLayout = new QFormLayout;
    settingLayout->addRow("Program", programEdit);
    settingLayout->addRow("Workspace", pathEdit);
    
    settingWidget = new QWidget(this);
    settingWidget->setLayout(settingLayout);
    
    tab = new QTabWidget(this);
    tab->addTab(settingWidget, "Setting");
}
