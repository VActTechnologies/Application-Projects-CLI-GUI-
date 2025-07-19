// temp_dashboard.cpp
#include <QApplication>
#include <QLabel>
#include <QTimer>
#include <QVBoxLayout>
#include <QWidget>
#include <QFile>

QString readCPUTemp() {
    QFile file("/sys/class/thermal/thermal_zone0/temp");
    if (file.open(QIODevice::ReadOnly)) {
        QByteArray tempData = file.readAll();
        file.close();
        bool ok;
        int milliC = tempData.trimmed().toInt(&ok);
        if (ok) return QString::number(milliC / 1000.0, 'f', 1) + " °C";
    }
    return "N/A";
}

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QLabel *tempLabel = new QLabel("Loading...", nullptr);
    tempLabel->setAlignment(Qt::AlignCenter);
    tempLabel->setStyleSheet("font-size: 24px;");

    QWidget window;
    QVBoxLayout *layout = new QVBoxLayout(&window);
    layout->addWidget(tempLabel);

    QTimer *timer = new QTimer();
    QObject::connect(timer, &QTimer::timeout, [&]() {
        tempLabel->setText("CPU Temp: " + readCPUTemp());
    });
    timer->start(1000); // update every second

    window.setWindowTitle("Temperature Dashboard");
    window.resize(300, 100);
    window.show();

    return app.exec();
}

