//
//  inspector.cpp
//  PyAircraft
//
//  Created by 田中伟 on 2017/4/30.
//  Copyright © 2017年 田中伟. All rights reserved.
//

#include "inspector.h"

Inspector::Inspector(QWidget *parent)
    : QTreeView(parent)
{
    setWindowTitle("Inspector");
    setObjectName("Inspector");
    
    model = new QStandardItemModel(0,2,this);
    model->setHeaderData(0, Qt::Horizontal, "Item");
    model->setHeaderData(1, Qt::Horizontal, "Value");
    
    setModel(model);
    setAlternatingRowColors(true);
    setUniformRowHeights(false);
}

Inspector::~Inspector()
{
    
}

void Inspector::setContent(QDomElement &parent)
{
    model->removeRows(0, model->rowCount());    
    appendChild(parent, QModelIndex());
}

void Inspector::appendChild(QDomElement &parent, QModelIndex parentIndex)
{
    if (parentIndex.isValid())
        model->insertColumns(0, 2, parentIndex);
    
    QDomElement element = parent.firstChildElement();
    while (!element.isNull())
    {
        int row = model->rowCount(parentIndex);
        model->insertRow(row, parentIndex);
        
        QModelIndex index0 = model->index(row,0,parentIndex);
        QModelIndex index1 = index0.sibling(row, 1);
        
        model->setData(index0, element.tagName());
        
        if (element.hasChildNodes() && element.firstChild().isText())
            model->setData(index1, element.text());
        else
            setFirstColumnSpanned(row, parentIndex, true);
        
        QStringList strs;
        QDomNamedNodeMap attrs = element.attributes();
        for(int i=0;i<attrs.size();i++)
        {
            QDomNode node = attrs.item(i);
            strs << QString("%1=%2").arg(node.nodeName()).arg(node.nodeValue());
        }
        
        model->setData(index0, strs.join("\n"), Qt::ToolTipRole);
        
        if (element.hasChildNodes())
            appendChild(element, index0);
        
        element = element.nextSiblingElement();
    }
}
