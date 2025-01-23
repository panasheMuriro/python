from plyer import notification

notification.notify(
    title='Test Notification',
    message='This is a test notification working on a macbook!',
    app_name='Python Auto',
    timeout=10  # duration in seconds
)