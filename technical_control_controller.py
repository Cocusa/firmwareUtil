from models.technical_control_model import ControlInfo, Stage, Status
from ui.process_output_ui import Output
from ui.table_ui import ControlProcessTable


stage_names = {
    Stage.ERPSn: "Поиск S/N прибора в ERP",
    Stage.ERPOrder: "Поиск S/N прибора в  заказах",
    Stage.Device: "Подключение прибора к ПО ВАЦ-ОТК",
    Stage.CheckContext: "Подключенный прибор соответствует заказу",
    Stage.CheckCalibration: "Статус заводской калибровки",
    Stage.CheckVnapn: "Наличие протокола VNAPT",
    Stage.Firmware: "Программирование варианта исполнения",
    Stage.LoadLicense: "Загрузка файлов лицензий из базы",
    Stage.LoadFeature: "Загрузка файлов дополнительных лицензий",
    Stage.CopyFiles: "Копирование файлов на flash-диск",
    Stage.SaveDump: "Сохранение дампа EEPROM в ERP",
    Stage.SaveReport: "Сохранение протокола 123 в ERP",
}


bootstyles = {
    Status.Failed: "inverse-danger",
    Status.InProgress: "inverse-primary",
    Status.Success: "inverse-success",
}


statuses_names = {
    Status.Failed: "ОШИБКА",
    Status.InProgress: "ВЫПОЛНЯЕТСЯ",
    Status.Success: "ОК",
}


def get_technical_control_table(master) -> ControlProcessTable:
    table = ControlProcessTable(master)

    for s in Stage:
        table.add(s, stage_names[s], "")

    return table


def get_technical_contol_output(master) -> Output:
    output = Output(master)
    output.set_tag("error", foreground="red", font=("TkDefaultFont", 15))
    output.set_tag("done", foreground="green", font=("TkDefaultFont", 15))
    return output


def change_contol_stage(table: ControlProcessTable, output: Output, stage: ControlInfo):
    table.change_bootstyle(stage.stage, bootstyle=bootstyles[stage.status])
    table.change_text(stage.stage, 1, statuses_names[stage.status])
    if stage.error is not None:
        output.next(stage.error.text, "error")
        output.next(stage.error.hint, "error")
    if stage.stage == Stage.SaveReport and stage.status == Status.Success:
        output.next("Проверка успешно завершена", "done")


def reset_control_table(table: ControlProcessTable):
    for s in Stage:
        table.change_bootstyle(s, bootstyle="default")
        table.change_text(s, 1, "")
