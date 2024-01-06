import  sys
from PyQt5.QtWidgets import QApplication,QMainWindow
import op
class Tree:
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.operator = ''
        self.context = ''
        self.attribute = ''
def split(sql):
    sql=sql.split()
    tree=Tree()
    index=0
    while True:
        if index>=len(sql):
            break
        elif sql[index]=='SELECT' or sql[index]=='PROJECTION':
            tree.operator=sql[index]
            index=index+2 #select->0 [->1
            context=''
            while sql[index]!=']':
                context+=sql[index]
                context+=' '
                index+=1
            index+=1
            tree.context=context
        elif sql[index]=='(':
            index+=1
            context_1=''
            count=0
            for i in (sql[index:]):
                if i=='(':
                    count=1
            while  sql[index]!=')'and count==0:
                context_1+=sql[index]
                context_1+=' '
                index+=1
            while  count==1:
                while sql[index]!=')':
                    context_1+=sql[index]
                    context_1+=' '
                    index+=1
                context_1+=sql[index]
                count=0
            index+=1
            tree.left_child=split(context_1)
        elif sql[index]=='JOIN':
            tree.operator=sql[index]
            tree.left_child=Tree()
            tree.left_child.attribute=sql[index-1]
            tree.right_child=Tree()
            tree.right_child.attribute=sql[index+1]
            index+=1
        else:
            index+=1
    return tree

def optimize(syntax_tree, sql):
    if syntax_tree.operator == 'SELECT':
        context = syntax_tree.context
        #拆开条件,并把条件向下传递
        sql = context.split('&')

        syntax_tree = optimize(syntax_tree.left_child, sql)
    elif syntax_tree.operator == 'PROJECTION':
        syntax_tree.left_child = optimize(syntax_tree.left_child, sql)
    elif syntax_tree.operator == 'JOIN':
        first_tree = Tree()
        first_tree.operator = 'SELECT'
        first_tree.context = sql[0]
        first_tree.left_child = syntax_tree.left_child
        syntax_tree.left_child = first_tree
        if len(sql) == 1:
            return syntax_tree
        second_tree = Tree()
        second_tree.operator = 'SELECT'
        second_tree.context = sql[1]
        second_tree.right_child = syntax_tree.right_child
        syntax_tree.right_child = second_tree
    return syntax_tree


def visualize(syntax_tree):
    global indent
    if syntax_tree.operator != '':
        ui.textEdit.append(" "*indent+syntax_tree.operator+"  "+syntax_tree.context)
    else:
        ui.textEdit.append(" "*indent+syntax_tree.attribute.replace(")",""))
    if syntax_tree.left_child is not None:
        indent = indent+2
        visualize(syntax_tree.left_child)
        indent = indent-2
    if syntax_tree.right_child is not None:
        indent = indent+2
        visualize(syntax_tree.right_child)
        indent = indent-2
def show():
    ui.lineEdit.setText(ui.select.currentText())
def after():
    #sql=ui.lineEdit.text()
    sql=ui.select.currentText()
    ui.textEdit.clear()
    ui.textEdit.append("优化前：")
    tree1=split(sql)
    visualize(tree1)
    ui.textEdit.append("优化后：")
    tree2=optimize(tree1,'')
    visualize(tree2)
if __name__=='__main__':
    indent=0
    app=QApplication(sys.argv)
    MainWindow=QMainWindow()
    ui=op.Ui_Dialog()
    ui.setupUi(MainWindow)
   # ui.show.clicked.connect(show)

    ui.pushButton_2.clicked.connect(after)

    MainWindow.show()
    sys.exit(app.exec_())








