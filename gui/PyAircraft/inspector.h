//
//  inspector.hpp
//  PyAircraft
//
//  Created by 田中伟 on 2017/4/30.
//  Copyright © 2017年 田中伟. All rights reserved.
//

#ifndef inspector_hpp
#define inspector_hpp

#include <QtWidgets>
#include <QtXml>

class Inspector : public QTreeView
{
    Q_OBJECT
    
public:
    Inspector(QWidget *parent=NULL);
    ~Inspector();
    
    void setContent(QDomElement &parent);
    
private:
    void appendChild(QDomElement &parent, QModelIndex parentIndex);

    QStandardItemModel *model;
};

#endif /* inspector_hpp */
