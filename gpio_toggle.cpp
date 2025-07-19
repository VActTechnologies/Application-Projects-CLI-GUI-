// gpio_toggle.cpp
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>
#include <QApplication>
#include <QFile>
#include <QTextStream>

void writeGPIO(int pin, const QString &value) {
    QFile file(QString("/sys/class/gpio/gpio%1/value").arg(pin));
    if (file.open(QIODevice::WriteOnly)) {
        QTextStream out(&file);
        out << value;
    }
}

void exportGPIO(int pin) {
    QFile exportFile("/sys/class/gpio/export");
    if (exportFile.open(QIODevice::WriteOnly)) {
        QTextStream out(&exportFile);
        out << pin;
    }
    QFile direction(QString("/sys/class/gpio/gpio%1/direction").arg(pin));
    if (direction.open(QIODevice::WriteOnly)) {
        QTextStream out(&direction);
        out << "out";
    }
}

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    int pin = 17; // GPIO17
    exportGPIO(pin);

    QPushButton *onButton = new QPushButton("LED ON");
    QPushButton *offButton = new QPushButton("LED OFF");

    QObject::connect(onButton, &QPushButton::clicked, [=]() {
        writeGPIO(pin, "1");
    });
    QObject::connect(offButton, &QPushButton::clicked, [=]() {
        writeGPIO(pin, "0");
    });

    QWidget window;
    QVBoxLayout *layout = new QVBoxLayout(&window);
    layout->addWidget(onButton);
    layout->addWidget(offButton);
    window.setWindowTitle("GPIO LED Toggle");
    window.show();

    return app.exec();
}

