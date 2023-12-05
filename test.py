import psutil
import osascript
import subprocess

def list_running_applications(target_apps):
    running_apps = []

    for app in psutil.process_iter(['pid', 'name']):
        try:
            app_info = app.info
            if app_info['name'].lower() in target_apps:
                running_apps.append(app_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # for app in psutil.process_iter(['pid', 'name']):
    #     try:
    #         app_info = app.info
    #         running_apps.append(app_info)
    #     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
    #         pass

    return running_apps

def mute_spotify():
    script = '''
    tell application "Spotify"
        set sound volume to 0
        end tell
        '''



def main():
    target_apps = ['arc', 'spotify', 'discord', 'google chorme']
    running_apps = list_running_applications(target_apps)

    print("Açık olan uygulamalar:")
    for i, app in enumerate(running_apps):
        print(f"{i}-{app['name']} (PID: {app['pid']})")

    selected_app_index = int(input("etkileşime geçilecek uygulama numara gir: "))

    if 0 <= selected_app_index < len(running_apps):
        selected_app_pid = running_apps[selected_app_index]['pid']
        print(f"Seçilen uygulama: {running_apps[selected_app_index]['name']} (PID: {selected_app_pid})")

        volume_option = input("Ses kontrolü için 'mute' veya 'unmute' seçiniz: ")

        if volume_option.lower() == 'mute':
            target_volume = 50
            osascript.osascript("set volume output volume {}".format(target_volume))
            mute_spotify()
            print(f"{running_apps[selected_app_index]['name']} uygulamasının sesi kapatıldı.")
            
        elif volume_option.lower() == 'unmute':
            # Burada seçilen uygulamanın sesini açma işlemi yapılabilir.
            print(f"{running_apps[selected_app_index]['name']} uygulamasının sesi açıldı.")
        else:
            print("Geçersiz ses kontrol seçeneği. 'mute' veya 'unmute' girin.")
    else:
        print("Geçersiz uygulama numarası.")

if __name__ == "__main__":
    main()
