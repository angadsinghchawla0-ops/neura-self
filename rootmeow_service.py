#!/usr/bin/env python3
"""
ROOTMEOW Android Foreground Service
Keeps the bot running in background on Android
"""

import os
import sys

# This file is used by buildozer for Android service
# The actual service implementation is handled by Kivy's python-for-android

SERVICE_NAME = "RootmeowService"
SERVICE_CLASS = "org.rootmeow.ServiceRootmeow"

# Android service boilerplate for p4a
# This gets compiled into the APK as a foreground service

def start_service():
    """Start the foreground service on Android"""
    try:
        from android import PythonService
        from android.permissions import request_permissions, Permission
        from jnius import autoclass

        PythonService = autoclass('org.kivy.android.PythonService')
        service = PythonService.mService

        # Set foreground notification
        Notification = autoclass('android.app.Notification')
        NotificationCompat = autoclass('androidx.core.app.NotificationCompat')
        NotificationManager = autoclass('android.app.NotificationManager')
        Context = autoclass('android.content.Context')
        Intent = autoclass('android.content.Intent')
        PendingIntent = autoclass('android.app.PendingIntent')

        # Create notification channel
        CHANNEL_ID = "rootmeow_channel"
        CHANNEL_NAME = "ROOTMEOW Bot"
        Build = autoclass('android.os.Build')
        if Build.VERSION.SDK_INT >= Build.VERSION_CODES.O:
            NotificationChannel = autoclass('android.app.NotificationChannel')
            channel = NotificationChannel(CHANNEL_ID, CHANNEL_NAME, NotificationManager.IMPORTANCE_LOW)
            manager = service.getSystemService(Context.NOTIFICATION_SERVICE)
            manager.createNotificationChannel(channel)

        # Build notification
        builder = NotificationCompat.Builder(service, CHANNEL_ID)
        builder.setContentTitle("ROOTMEOW Running")
        builder.setContentText("Discord bot is active in background")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        builder.setOngoing(True)
        builder.setPriority(NotificationCompat.PRIORITY_LOW)

        # Start foreground
        service.startForeground(1, builder.build())

    except Exception as e:
        print(f"Service start error: {e}")

def stop_service():
    """Stop the foreground service"""
    try:
        from android import PythonService
        PythonService = autoclass('org.kivy.android.PythonService')
        service = PythonService.mService
        service.stopForeground(True)
        service.stopSelf()
    except Exception as e:
        print(f"Service stop error: {e}")

if __name__ == "__main__":
    start_service()
    # Keep service alive
    import time
    while True:
        time.sleep(60)