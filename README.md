# Rocket Launch

Welcome to Rocket Launch Bot!

## Description.

We have a video of a rocket launch and we want to know in which frame exactly the rocket is launched using a **Telegram Bot** and the **BERNARD** framework.

## Configuration

To run this code it is recommended to follow the following steps
1. Use a virtual environment such as **Virtualenv**. Configure the environment with **Python3.6** and **Pip=9.0.3**.
2. Install Bernard in the environment. If you need help to continue, refer to the [BERNARD documentation](https://github.com/BernardFW/bernard). 
3. A Redis database is required, so you will need to start it using
   ``sh
      redis-server
    ``` 
5. The bot needs a public URL. **Ngrok** is the solution. Note: Port 8443 is one of the available ports for Telegram.
    ````sh
      ./ngrok http 8443
    ```  
7. Create your Bernard project:
    ````sh
      bernard start_project launch_rocket ./dev/launch_rocket
    ``` 
6. Create your Bot using BotFather in Telegram [Telegram Bot's documentation](https://core.telegram.org/bots) 
7. Configure your env file:
  - Set the **TELEGRAM_TOKEN** token obtained from BotFather (mandatory to use that name).
  - Set the **BIND_PORT**=8443 Use one of the available ports for Telegram
  - Set the **BERNARD_BASE_URL** (the public URL of Ngrok)
8. Run the program. In the main folder, run the commands
    ``sh
      source ./env
      ./manage.py run
    ```  

 You should be able to use your bot. 

## System description

1. Inside the rocket_launch/src folder we can find the following: 

* ** **states.py**: Defines all possible states that our finite state machine can perform. 
** **transitions.py**: Defines all the possible transitions between states of our FSM.
**frames.py**: Useful methods to obtain frame information. 
** **bisection.py**: Performs the bisection for the new frame.
**environment.py**: Contains the video variables.   
** **trigger.py**: Detects when the guessig is finished using the `is_finished` parameter. Once the guessig is finished the result is displayed.  

2. Inside the i18/end folder we can find the following:
* **intents.csv**: File to understand the possible different user responses.  
** **responses.cv**: Contains all the predefined responses for our bot.   

