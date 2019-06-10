from quart import Quart, render_template, request
import subprocess, asyncio

app = Quart(__name__)

def av( choice, url ):
    if choice == 'video' and len(url):
        try:
            x = subprocess.run([ 'youtube-dl' , url ], shell=True)
            return "Downloaded video successfully"
        except Exception as e:
            return f"Error while processing the URL : {url} as {e}"
    if choice == "audio" and len(url):
        try:
            x = subprocess.run([ 'youtube-dl' , '-x' , '--audio-format' , 'best' , url ], shell=True)
            return "Downloaded audio successfully"
        except Exception as e:
            return f"Error while processing the URL : {url} as {e}" 
    else:
        return "Invalid input parameters"

class BackgroundTask:
    async def run(self, coro, args, callback=None):
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self.task_runner, coro, args, callback)

    def task_runner(self, coro, args, callback):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            fut = asyncio.ensure_future(coro(*args))
            if callback is not None:
                fut.add_done_callback(callback)
            loop.run_until_complete(fut)
            loop.close()
        except Exception as e:
            print(e)

@app.route('/tube', methods=['GET', "POST"])
async def index():
    if request.method == 'GET':
        return await render_template('index.html')

    elif request.method == 'POST':
        inputs = await request.form
        choice = inputs.get( 'choice', "" )
        url = inputs.get( 'url', "" )
        bg_task = BackgroundTask()
        args = ( choice, url )
        callback = None
        
        try:
            status = await bg_task.run(av, args, callback )
            print ( status )
        except Exception as e:
            print(e)
        
        return '''
                    <script>
                        alert("Added to download queue successfully");
                        window.location = "/tube";
                    </script>
                '''

    return 'Invalid Method'        

app.run( debug=False, host='0.0.0.0', port=80 )