#include <iostream>
using namespace std;

// 计算单个课程的绩点
double calculateGPA(double grade, double credit) {
    if (grade < 60) {
        return 0;
    } else {
        return ((grade - 50) / 10.0) * credit;
    }
}

// 清屏函数，针对不同平台的实现
void clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

int main() {
    while (true) {
        double grade, credit;
        double totalGPA = 0;
        double totalCredits = 0;
        
        cout << "请输入你的课程分数和学分 (结束请输入0 0):" << endl;

        while (true) {
            cin >> grade >> credit;
            if (grade == 0 && credit == 0) {
                break;
            }
            totalGPA += calculateGPA(grade, credit);
            totalCredits += credit;
        }

        if (totalCredits == 0) {
            cout << "没有有效的课程输入." << endl;
        } else {
            double finalGPA = totalGPA / totalCredits;
            cout << "总绩点为: " << finalGPA << endl;
        }

        char choice;
        cout << "你想继续计算吗？(y/n): ";
        cin >> choice;

        if (choice == 'n' || choice == 'N') {
            break;
        } else if (choice == 'y' || choice == 'Y') {
            clearScreen();  // 清屏
        } else {
            cout << "无效的输入，程序将退出." << endl;
            break;
        }
    }

    return 0;
}
