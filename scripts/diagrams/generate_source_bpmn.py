# -*- coding: utf-8 -*-
"""
Генерация исходных BPMN 2.0 XML файлов (.bpmn)
для открытия в bpmn.io и Camunda Modeler
"""

import os

bpmn_1_as_is = """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
                  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
                  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
                  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
                  id="Definitions_Order_AsIs"
                  targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn:collaboration id="Collaboration_1">
    <bpmn:participant id="Participant_Confectionery" name="Кондитерская «SweetCraft» (Процесс As-Is)" processRef="Process_Order_AsIs" />
  </bpmn:collaboration>
  <bpmn:process id="Process_Order_AsIs" isExecutable="false">
    <bpmn:laneSet id="LaneSet_1">
      <bpmn:lane id="Lane_Customer" name="Клиент (Покупатель)">
        <bpmn:flowNodeRef>Start_NeedCake</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_SendWhatsApp</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_ClarifyDetails</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_PayPrepayment</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>End_RefusalPrice</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_Manager" name="Менеджер заказов">
        <bpmn:flowNodeRef>Task_ReadMessage</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_CalcPriceManual</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_AskBaker</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_CustomerAgrees</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_CheckBank</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_WriteSticker</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_Baker" name="Шеф-кондитер цеха">
        <bpmn:flowNodeRef>Task_CheckJournal</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_CapacityOk</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>End_OverloadRefusal</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>End_OrderOnSticker</bpmn:flowNodeRef>
      </bpmn:lane>
    </bpmn:laneSet>
    
    <bpmn:startEvent id="Start_NeedCake" name="Возникла потребность в торте">
      <bpmn:outgoing>Flow_1</bpmn:outgoing>
    </bpmn:startEvent>
    <bpmn:task id="Task_SendWhatsApp" name="Отправить запрос с фото в WhatsApp">
      <bpmn:incoming>Flow_1</bpmn:incoming>
      <bpmn:outgoing>Flow_2</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_ReadMessage" name="Прочитать сообщение и запросить детали">
      <bpmn:incoming>Flow_2</bpmn:incoming>
      <bpmn:outgoing>Flow_3</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_ClarifyDetails" name="Ответить на вопросы о весе и начинке">
      <bpmn:incoming>Flow_3</bpmn:incoming>
      <bpmn:outgoing>Flow_4</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_CalcPriceManual" name="Вручную рассчитать цену на калькуляторе">
      <bpmn:incoming>Flow_4</bpmn:incoming>
      <bpmn:outgoing>Flow_5</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_AskBaker" name="Пойти в цех и спросить о загрузке">
      <bpmn:incoming>Flow_5</bpmn:incoming>
      <bpmn:outgoing>Flow_6</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_CheckJournal" name="Проверить записи в бумажном журнале">
      <bpmn:incoming>Flow_6</bpmn:incoming>
      <bpmn:outgoing>Flow_7</bpmn:outgoing>
    </bpmn:task>
    <bpmn:exclusiveGateway id="Gateway_CapacityOk" name="Успеем выпечь на дату?">
      <bpmn:incoming>Flow_7</bpmn:incoming>
      <bpmn:outgoing>Flow_Overload</bpmn:outgoing>
      <bpmn:outgoing>Flow_CapacityYes</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:endEvent id="End_OverloadRefusal" name="Отказ клиенту: цех перегружен">
      <bpmn:incoming>Flow_Overload</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:exclusiveGateway id="Gateway_CustomerAgrees" name="Клиент согласен с ценой?">
      <bpmn:incoming>Flow_CapacityYes</bpmn:incoming>
      <bpmn:outgoing>Flow_PriceNo</bpmn:outgoing>
      <bpmn:outgoing>Flow_PriceYes</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:endEvent id="End_RefusalPrice" name="Отказ клиента из-за цены">
      <bpmn:incoming>Flow_PriceNo</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:task id="Task_PayPrepayment" name="Перевести 50% предоплаты по номеру карты">
      <bpmn:incoming>Flow_PriceYes</bpmn:incoming>
      <bpmn:outgoing>Flow_8</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_CheckBank" name="Проверить перевод в мобильном банке">
      <bpmn:incoming>Flow_8</bpmn:incoming>
      <bpmn:outgoing>Flow_9</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_WriteSticker" name="Записать заказ в журнал и выписать стикер">
      <bpmn:incoming>Flow_9</bpmn:incoming>
      <bpmn:outgoing>Flow_10</bpmn:outgoing>
    </bpmn:task>
    <bpmn:endEvent id="End_OrderOnSticker" name="Заказ зафиксирован в цеху на стикере">
      <bpmn:incoming>Flow_10</bpmn:incoming>
    </bpmn:endEvent>

    <bpmn:sequenceFlow id="Flow_1" sourceRef="Start_NeedCake" targetRef="Task_SendWhatsApp" />
    <bpmn:sequenceFlow id="Flow_2" sourceRef="Task_SendWhatsApp" targetRef="Task_ReadMessage" />
    <bpmn:sequenceFlow id="Flow_3" sourceRef="Task_ReadMessage" targetRef="Task_ClarifyDetails" />
    <bpmn:sequenceFlow id="Flow_4" sourceRef="Task_ClarifyDetails" targetRef="Task_CalcPriceManual" />
    <bpmn:sequenceFlow id="Flow_5" sourceRef="Task_CalcPriceManual" targetRef="Task_AskBaker" />
    <bpmn:sequenceFlow id="Flow_6" sourceRef="Task_AskBaker" targetRef="Task_CheckJournal" />
    <bpmn:sequenceFlow id="Flow_7" sourceRef="Task_CheckJournal" targetRef="Gateway_CapacityOk" />
    <bpmn:sequenceFlow id="Flow_Overload" name="[Перегруз цеха]" sourceRef="Gateway_CapacityOk" targetRef="End_OverloadRefusal" />
    <bpmn:sequenceFlow id="Flow_CapacityYes" name="[Свободно]" sourceRef="Gateway_CapacityOk" targetRef="Gateway_CustomerAgrees" />
    <bpmn:sequenceFlow id="Flow_PriceNo" name="[Дорого]" sourceRef="Gateway_CustomerAgrees" targetRef="End_RefusalPrice" />
    <bpmn:sequenceFlow id="Flow_PriceYes" name="[Согласен]" sourceRef="Gateway_CustomerAgrees" targetRef="Task_PayPrepayment" />
    <bpmn:sequenceFlow id="Flow_8" sourceRef="Task_PayPrepayment" targetRef="Task_CheckBank" />
    <bpmn:sequenceFlow id="Flow_9" sourceRef="Task_CheckBank" targetRef="Task_WriteSticker" />
    <bpmn:sequenceFlow id="Flow_10" sourceRef="Task_WriteSticker" targetRef="End_OrderOnSticker" />
  </bpmn:process>
</bpmn:definitions>
"""

bpmn_2_to_be = """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
                  id="Definitions_Order_ToBe"
                  targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn:collaboration id="Collaboration_2">
    <bpmn:participant id="Participant_Confectionery_ToBe" name="Кондитерская «SweetCraft» (Процесс To-Be)" processRef="Process_Order_ToBe" />
  </bpmn:collaboration>
  <bpmn:process id="Process_Order_ToBe" isExecutable="true">
    <bpmn:laneSet id="LaneSet_2">
      <bpmn:lane id="Lane_Customer_ToBe" name="Клиент (Покупатель)">
        <bpmn:flowNodeRef>Start_ToBe</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_SelectParams</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_UploadAndSubmit</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_System_ToBe" name="Веб-сервис Django (Бэкенд)">
        <bpmn:flowNodeRef>Task_AsyncCalc</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_LimitCheck</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_ShowWarning</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_ShowPrice</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_SaveAtomic</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_GenDocAndEmail</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_Baker_ToBe" name="Шеф-кондитер цеха">
        <bpmn:flowNodeRef>Task_PrintTechCard</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>End_SuccessToBe</bpmn:flowNodeRef>
      </bpmn:lane>
    </bpmn:laneSet>
    
    <bpmn:startEvent id="Start_ToBe" name="Переход в онлайн-конструктор">
      <bpmn:outgoing>Flow_T1</bpmn:outgoing>
    </bpmn:startEvent>
    <bpmn:task id="Task_SelectParams" name="Выбрать вес, начинку, корж и дату выдачи">
      <bpmn:incoming>Flow_T1</bpmn:incoming>
      <bpmn:incoming>Flow_RetryDate</bpmn:incoming>
      <bpmn:outgoing>Flow_T2</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_AsyncCalc" name="Рассчитать цену и проверить лимит цеха (fetch API)">
      <bpmn:incoming>Flow_T2</bpmn:incoming>
      <bpmn:outgoing>Flow_T3</bpmn:outgoing>
    </bpmn:task>
    <bpmn:exclusiveGateway id="Gateway_LimitCheck" name="Суточный лимит смены превышен?">
      <bpmn:incoming>Flow_T3</bpmn:incoming>
      <bpmn:outgoing>Flow_LimitOver</bpmn:outgoing>
      <bpmn:outgoing>Flow_LimitOk</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:task id="Task_ShowWarning" name="Вывести предупреждение и заблокировать дату">
      <bpmn:incoming>Flow_LimitOver</bpmn:incoming>
      <bpmn:outgoing>Flow_RetryDate</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_ShowPrice" name="Отобразить расчетную цену и статус даты">
      <bpmn:incoming>Flow_LimitOk</bpmn:incoming>
      <bpmn:outgoing>Flow_T4</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_UploadAndSubmit" name="Загрузить эскиз (до 5 МБ) и нажать «Оформить заказ»">
      <bpmn:incoming>Flow_T4</bpmn:incoming>
      <bpmn:outgoing>Flow_T5</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_SaveAtomic" name="Зафиксировать заказ в БД (transaction.atomic)">
      <bpmn:incoming>Flow_T5</bpmn:incoming>
      <bpmn:outgoing>Flow_T6</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_GenDocAndEmail" name="Сгенерировать техкарту и отправить email клиенту">
      <bpmn:incoming>Flow_T6</bpmn:incoming>
      <bpmn:outgoing>Flow_T7</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_PrintTechCard" name="Распечатать техкарту и выпекать по рецептуре">
      <bpmn:incoming>Flow_T7</bpmn:incoming>
      <bpmn:outgoing>Flow_T8</bpmn:outgoing>
    </bpmn:task>
    <bpmn:endEvent id="End_SuccessToBe" name="Заказ принят в цех с гарантией брони веса">
      <bpmn:incoming>Flow_T8</bpmn:incoming>
    </bpmn:endEvent>

    <bpmn:sequenceFlow id="Flow_T1" sourceRef="Start_ToBe" targetRef="Task_SelectParams" />
    <bpmn:sequenceFlow id="Flow_T2" sourceRef="Task_SelectParams" targetRef="Task_AsyncCalc" />
    <bpmn:sequenceFlow id="Flow_T3" sourceRef="Task_AsyncCalc" targetRef="Gateway_LimitCheck" />
    <bpmn:sequenceFlow id="Flow_LimitOver" name="[Да, перегруз]" sourceRef="Gateway_LimitCheck" targetRef="Task_ShowWarning" />
    <bpmn:sequenceFlow id="Flow_RetryDate" sourceRef="Task_ShowWarning" targetRef="Task_SelectParams" />
    <bpmn:sequenceFlow id="Flow_LimitOk" name="[Нет, свободно]" sourceRef="Gateway_LimitCheck" targetRef="Task_ShowPrice" />
    <bpmn:sequenceFlow id="Flow_T4" sourceRef="Task_ShowPrice" targetRef="Task_UploadAndSubmit" />
    <bpmn:sequenceFlow id="Flow_T5" sourceRef="Task_UploadAndSubmit" targetRef="Task_SaveAtomic" />
    <bpmn:sequenceFlow id="Flow_T6" sourceRef="Task_SaveAtomic" targetRef="Task_GenDocAndEmail" />
    <bpmn:sequenceFlow id="Flow_T7" sourceRef="Task_GenDocAndEmail" targetRef="Task_PrintTechCard" />
    <bpmn:sequenceFlow id="Flow_T8" sourceRef="Task_PrintTechCard" targetRef="End_SuccessToBe" />
  </bpmn:process>
</bpmn:definitions>
"""

bpmn_3_shifts = """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
                  id="Definitions_Shifts_ToBe"
                  targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn:collaboration id="Collaboration_3">
    <bpmn:participant id="Participant_Shifts" name="Процесс 2: Планирование смен и лимитов выпечки цеха" processRef="Process_Shifts" />
  </bpmn:collaboration>
  <bpmn:process id="Process_Shifts" isExecutable="true">
    <bpmn:laneSet id="LaneSet_3">
      <bpmn:lane id="Lane_Chef" name="Шеф-кондитер / Управляющий">
        <bpmn:flowNodeRef>Start_ShiftPeriod</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_OpenShiftPanel</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_SelectDateAndBaker</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_HolidayCheck</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_SetHolidayLimit</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_SetStandardLimit</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_ClickSaveShift</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_System_Shifts" name="Веб-сервис Django (Бэкенд)">
        <bpmn:flowNodeRef>Task_SaveShiftDB</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_UpdateQuotas</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>End_ShiftsUpdated</bpmn:flowNodeRef>
      </bpmn:lane>
    </bpmn:laneSet>
    
    <bpmn:startEvent id="Start_ShiftPeriod" name="Наступление периода планирования">
      <bpmn:outgoing>Flow_S1</bpmn:outgoing>
    </bpmn:startEvent>
    <bpmn:task id="Task_OpenShiftPanel" name="Открыть панель смен в админ-разделе">
      <bpmn:incoming>Flow_S1</bpmn:incoming>
      <bpmn:outgoing>Flow_S2</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_SelectDateAndBaker" name="Выбрать дату смены и дежурного кондитера">
      <bpmn:incoming>Flow_S2</bpmn:incoming>
      <bpmn:outgoing>Flow_S3</bpmn:outgoing>
    </bpmn:task>
    <bpmn:exclusiveGateway id="Gateway_HolidayCheck" name="Смена в праздничный/выходной день?">
      <bpmn:incoming>Flow_S3</bpmn:incoming>
      <bpmn:outgoing>Flow_HolidayYes</bpmn:outgoing>
      <bpmn:outgoing>Flow_HolidayNo</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:task id="Task_SetHolidayLimit" name="Установить повышенный лимит (45 кг)">
      <bpmn:incoming>Flow_HolidayYes</bpmn:incoming>
      <bpmn:outgoing>Flow_S4a</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_SetStandardLimit" name="Установить стандартный лимит (35 кг)">
      <bpmn:incoming>Flow_HolidayNo</bpmn:incoming>
      <bpmn:outgoing>Flow_S4b</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_ClickSaveShift" name="Нажать «Сохранить смену»">
      <bpmn:incoming>Flow_S4a</bpmn:incoming>
      <bpmn:incoming>Flow_S4b</bpmn:incoming>
      <bpmn:outgoing>Flow_S5</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_SaveShiftDB" name="Записать объект ConfectionerShift в БД">
      <bpmn:incoming>Flow_S5</bpmn:incoming>
      <bpmn:outgoing>Flow_S6</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_UpdateQuotas" name="Обновить доступные квоты для конструктора заказов">
      <bpmn:incoming>Flow_S6</bpmn:incoming>
      <bpmn:outgoing>Flow_S7</bpmn:outgoing>
    </bpmn:task>
    <bpmn:endEvent id="End_ShiftsUpdated" name="Производственные лимиты смен актуализированы">
      <bpmn:incoming>Flow_S7</bpmn:incoming>
    </bpmn:endEvent>

    <bpmn:sequenceFlow id="Flow_S1" sourceRef="Start_ShiftPeriod" targetRef="Task_OpenShiftPanel" />
    <bpmn:sequenceFlow id="Flow_S2" sourceRef="Task_OpenShiftPanel" targetRef="Task_SelectDateAndBaker" />
    <bpmn:sequenceFlow id="Flow_S3" sourceRef="Task_SelectDateAndBaker" targetRef="Gateway_HolidayCheck" />
    <bpmn:sequenceFlow id="Flow_HolidayYes" name="[Да]" sourceRef="Gateway_HolidayCheck" targetRef="Task_SetHolidayLimit" />
    <bpmn:sequenceFlow id="Flow_HolidayNo" name="[Нет]" sourceRef="Gateway_HolidayCheck" targetRef="Task_SetStandardLimit" />
    <bpmn:sequenceFlow id="Flow_S4a" sourceRef="Task_SetHolidayLimit" targetRef="Task_ClickSaveShift" />
    <bpmn:sequenceFlow id="Flow_S4b" sourceRef="Task_SetStandardLimit" targetRef="Task_ClickSaveShift" />
    <bpmn:sequenceFlow id="Flow_S5" sourceRef="Task_ClickSaveShift" targetRef="Task_SaveShiftDB" />
    <bpmn:sequenceFlow id="Flow_S6" sourceRef="Task_SaveShiftDB" targetRef="Task_UpdateQuotas" />
    <bpmn:sequenceFlow id="Flow_S7" sourceRef="Task_UpdateQuotas" targetRef="End_ShiftsUpdated" />
  </bpmn:process>
</bpmn:definitions>
"""

bpmn_4_fulfillment = """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
                  id="Definitions_Fulfillment_ToBe"
                  targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn:collaboration id="Collaboration_4">
    <bpmn:participant id="Participant_Fulfillment" name="Процесс 3: Выдача готового изделия и сбор отзывов" processRef="Process_Fulfillment" />
  </bpmn:collaboration>
  <bpmn:process id="Process_Fulfillment" isExecutable="true">
    <bpmn:laneSet id="LaneSet_4">
      <bpmn:lane id="Lane_Baker_Fulf" name="Кондитер цеха (Мастер)">
        <bpmn:flowNodeRef>Start_ReadyCake</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_PackAndSetReady</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_HandoverCake</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_SetCompleted</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_Customer_Fulf" name="Клиент (Покупатель)">
        <bpmn:flowNodeRef>Task_ArriveBakery</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_ReviewChoice</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_WriteReview</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>End_NoReview</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_System_Fulf" name="Веб-сервис Django (Бэкенд)">
        <bpmn:flowNodeRef>Task_SendEmailReady</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_PublishReview</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>End_OrderFinishedAndRated</bpmn:flowNodeRef>
      </bpmn:lane>
    </bpmn:laneSet>
    
    <bpmn:startEvent id="Start_ReadyCake" name="Торт готов и охлажден в цеху">
      <bpmn:outgoing>Flow_F1</bpmn:outgoing>
    </bpmn:startEvent>
    <bpmn:task id="Task_PackAndSetReady" name="Упаковать торт и перевести статус в «Готов к выдаче»">
      <bpmn:incoming>Flow_F1</bpmn:incoming>
      <bpmn:outgoing>Flow_F2</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_SendEmailReady" name="Отправить клиенту email-уведомление о готовности">
      <bpmn:incoming>Flow_F2</bpmn:incoming>
      <bpmn:outgoing>Flow_F3</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_ArriveBakery" name="Прибыть в пункт выдачи кондитерской">
      <bpmn:incoming>Flow_F3</bpmn:incoming>
      <bpmn:outgoing>Flow_F4</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_HandoverCake" name="Сверить номер заказа и выдать торт клиенту">
      <bpmn:incoming>Flow_F4</bpmn:incoming>
      <bpmn:outgoing>Flow_F5</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_SetCompleted" name="Изменить статус заказа на «Выдан клиенту»">
      <bpmn:incoming>Flow_F5</bpmn:incoming>
      <bpmn:outgoing>Flow_F6</bpmn:outgoing>
    </bpmn:task>
    <bpmn:exclusiveGateway id="Gateway_ReviewChoice" name="Клиент желает оставить отзыв?">
      <bpmn:incoming>Flow_F6</bpmn:incoming>
      <bpmn:outgoing>Flow_RevNo</bpmn:outgoing>
      <bpmn:outgoing>Flow_RevYes</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:endEvent id="End_NoReview" name="Заказ закрыт без публикации отзыва">
      <bpmn:incoming>Flow_RevNo</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:task id="Task_WriteReview" name="Поставить оценку и написать отзыв на сайте">
      <bpmn:incoming>Flow_RevYes</bpmn:incoming>
      <bpmn:outgoing>Flow_F7</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Task_PublishReview" name="Сохранить отзыв Review в БД и опубликовать в каталоге">
      <bpmn:incoming>Flow_F7</bpmn:incoming>
      <bpmn:outgoing>Flow_F8</bpmn:outgoing>
    </bpmn:task>
    <bpmn:endEvent id="End_OrderFinishedAndRated" name="Заказ полностью закрыт и оценен клиентом">
      <bpmn:incoming>Flow_F8</bpmn:incoming>
    </bpmn:endEvent>

    <bpmn:sequenceFlow id="Flow_F1" sourceRef="Start_ReadyCake" targetRef="Task_PackAndSetReady" />
    <bpmn:sequenceFlow id="Flow_F2" sourceRef="Task_PackAndSetReady" targetRef="Task_SendEmailReady" />
    <bpmn:sequenceFlow id="Flow_F3" sourceRef="Task_SendEmailReady" targetRef="Task_ArriveBakery" />
    <bpmn:sequenceFlow id="Flow_F4" sourceRef="Task_ArriveBakery" targetRef="Task_HandoverCake" />
    <bpmn:sequenceFlow id="Flow_F5" sourceRef="Task_HandoverCake" targetRef="Task_SetCompleted" />
    <bpmn:sequenceFlow id="Flow_F6" sourceRef="Task_SetCompleted" targetRef="Gateway_ReviewChoice" />
    <bpmn:sequenceFlow id="Flow_RevNo" name="[Нет]" sourceRef="Gateway_ReviewChoice" targetRef="End_NoReview" />
    <bpmn:sequenceFlow id="Flow_RevYes" name="[Да]" sourceRef="Gateway_ReviewChoice" targetRef="Task_WriteReview" />
    <bpmn:sequenceFlow id="Flow_F7" sourceRef="Task_WriteReview" targetRef="Task_PublishReview" />
    <bpmn:sequenceFlow id="Flow_F8" sourceRef="Task_PublishReview" targetRef="End_OrderFinishedAndRated" />
  </bpmn:process>
</bpmn:definitions>
"""

with open("assets/diagrams/bpmn_order_as_is.bpmn", "w", encoding="utf-8") as f:
    f.write(bpmn_1_as_is.strip())

with open("assets/diagrams/bpmn_order_to_be.bpmn", "w", encoding="utf-8") as f:
    f.write(bpmn_2_to_be.strip())

with open("assets/diagrams/bpmn_shift_planning_to_be.bpmn", "w", encoding="utf-8") as f:
    f.write(bpmn_3_shifts.strip())

with open("assets/diagrams/bpmn_order_fulfillment_to_be.bpmn", "w", encoding="utf-8") as f:
    f.write(bpmn_4_fulfillment.strip())

print("All 4 source .bpmn XML files generated successfully!")
