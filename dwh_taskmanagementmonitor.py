"""
Task Management Monitor For DWH System Package
1. Main Parent Process will never end. Always running until a Keyboard Interrupt
2, Main Parent Process will create sub process
"""
import multiprocessing, time, os

def execute_sql(query):
    print("Executed Query:", query)


if __name__ == "__main__":
    while True:

        processes = []

        # 21 Times Process Execution
        for _ in range(21):
            sql_execute_process = multiprocessing.Process(target = execute_sql, args = ("SELECT * FROM TABLE",))
            sql_execute_process.start()
            processes.append(sql_execute_process)
            time.sleep(10)
            print("Parent Process:", os.getpid())

        for process in processes:
            process.join()

    
