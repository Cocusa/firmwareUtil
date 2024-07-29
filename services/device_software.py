import os
from models.models import PID, DeviceContext, DeviceVID, Software
import socketscpi
import time
import subprocess


soft_general_path = ".\softwares"

soft_names = {
    Software.SOFT1: "SOFT1",
}

soft_paths = {
    Software.SOFT1: f"{soft_general_path}\SOFT1.exe",
}

class DeviceCommunicator:
    port = 1111
    ipAddress = "1.1.1.1"

    def __init__(self, software: Software):
        self.software = software

        self._kill_all_soft_task()
        
        self.soft_process = self._run_software(software)

        time.sleep(0.2)

        self._wait_soft_init()

        if self.instrument is None or self.is_ready() == 0:
            raise SoftwareError(
                f"Не удалось подключиться к программному обеспечению устройства. {software.value} - {soft_paths[software]}."
            )

    def __del__(self):
        try:
            self.instrument.close()
            self._kill_all_soft_task()
        except Exception:
            pass

    def _kill_all_soft_task(self):
        soft_name = soft_names[self.software]
        error_code = os.system(f"taskkill /f /im  {soft_name}")
        if error_code != 0 and error_code != 128:
            raise Exception(
                f"Ошибка закрытия ПО - {soft_name}, код ошибки taskkill - {error_code}"
            )

    def _run_software(self, software: Software):
        if(software == Software.SOFT1 or software == Software.SOFT1):        
            return subprocess.Popen(
                [
                    soft_paths[software],
                    f"/SocketPort:{self.port}",
                    "/SocketServer:on",
                    "/restartmessage:off",
                    "/visible:off",
                ]
            )
        elif(software == Software.SOFT1 or software == Software.SOFT1):
            return subprocess.Popen(
                [
                    soft_paths[software],
                    f"/EnableSocket:{self.port}",
                    "/restartmessage:off",
                    "/InvisibleMode",
                ]
            )
        elif(software == Software.SOFT1):
            return subprocess.Popen(
                [
                    soft_paths[software],
                    "-e",
                    "--socketServer",
                    "On",
                    "--socketPort",
                    f"{self.port}",
                ]
            )
        elif(software == Software.SOFT1):
            return subprocess.Popen(
                [
                    soft_paths[software],
                    "--socketPort",
                    f"{self.port}",
                ]
            )
        else:
            raise SoftwareError("Неподдерживаемое ПО.")

    def _wait_soft_init(self):
        for i in range(3):
            try:
                time.sleep(5)
                self.instrument = socketscpi.SocketInstrument(
                    self.ipAddress, self.port
                )
                self.clear_error_queue()

                for i in range(3):
                    if self.is_ready() == 1:
                        break
                    time.sleep(1)

                break
            except ConnectionError as ex:
                time.sleep(0.2)

    # Read all errors until none are left. Generally, instruments return a message that begins with the string '0,"No error'.
    #написана своя реализация функции по скольку в ПО SOFT1 текст возвращаемый SYST:ERR отличен от других ПО.
    def clear_error_queue(self): 
        err = []
        no_error_text = self.get_no_error_text()

        temp = self.get_error().strip().replace('+', '').replace('-', '')

        while no_error_text not in temp:
            err.append(temp)
            temp = self.get_error().strip().replace('+', '').replace('-', '')
        if err:
            raise SoftwareError(err)

    def get_no_error_text(self):
        return 'no error'

    def get_device_context(self) -> DeviceContext:
        res = self.instrument.query("*IDN?")
        res = res.split(", ")
        return DeviceContext(
            manufacturer=res[0],
            #кодировка из библиотеки SCPI - latin_1
            model=bytes(res[1], encoding="latin_1").decode("cp1251"),
            serialNumber=res[2],
            version=res[3],
        )

    def set_manufacturing(self, manufacture: int):
        self.instrument.write(f"SERVice:cmd1:cmd1 {manufacture}")
        self.wait_last_command()

    def get_manufacturing(self):
        return self.instrument.query("SERVice:cmd1:cmd1?")
        
    def set_pid(self, pid: PID):
        self.instrument.write(f"SERVice:cmd1:cmd1 {pid.value}")
        self.wait_last_command()

    def get_pid(self):
        return PID(self.instrument.query("SERVice:cmd1:cmd1?"))
    
    def set_vid(self, vid: DeviceVID):        
        self.instrument.write(f"SERVice:cmd1:cmd1 {vid.value}")
        self.wait_last_command()

    def get_vid(self):
        return DeviceVID(self.instrument.query("SERVice:cmd1:cmd1?"))

    def save_backup(self, path: str):
        self.instrument.write(f'SERVice:cmd1:cmd1 "{path}"')
        self.wait_last_command()

    def is_ready(self):
        return int(self.instrument.query("SYST:READ?"))

    def get_test_device_result(self) -> str:
        return self.instrument.query("SYST:TEST?")

    def wait_last_command(self):
        return self.instrument.query("*OPC?")

    def get_error(self):
        return self.instrument.query("SYST:ERR?")

    def terminate(self):
        self.instrument.write("SYSTem:TERMinate")
        self.wait_last_command()


class SoftwareError(Exception):
    pass
