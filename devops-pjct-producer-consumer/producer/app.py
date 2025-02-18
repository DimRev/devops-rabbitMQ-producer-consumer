import schedule
import threading
import time
from flask import Flask

scheduler_started = False

def task():
    print('Done task')

def schedule_task():
    global scheduler_started
    if scheduler_started:
        return
    scheduler_started = True

    schedule.every(10).seconds.do(task)
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=schedule_task, daemon=True).start()

app = Flask(__name__)

@app.route('/healthz')
def healthz():
    return 'OK!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
