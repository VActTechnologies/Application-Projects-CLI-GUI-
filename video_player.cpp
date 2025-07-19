#include <QApplication>
#include <QMediaPlayer>
#include <QVideoWidget>
#include <QPushButton>
#include <QVBoxLayout>
#include <QFileDialog>
#include <QWidget>
#include <QUrl>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QWidget window;
    QVBoxLayout *layout = new QVBoxLayout(&window);

    QVideoWidget *videoWidget = new QVideoWidget;
    QMediaPlayer *player = new QMediaPlayer;

    QPushButton *openBtn = new QPushButton("Open Video");

    player->setVideoOutput(videoWidget);

    QObject::connect(openBtn, &QPushButton::clicked, [&]() {
        QString file = QFileDialog::getOpenFileName(nullptr, "Open Video");
        if (!file.isEmpty()) {
            player->setMedia(QUrl::fromLocalFile(file));  // Qt5-style
            player->play();
        }
    });

    layout->addWidget(videoWidget);
    layout->addWidget(openBtn);

    window.setWindowTitle("Qt5 Video Player");
    window.resize(640, 480);
    window.show();

    return app.exec();
}

