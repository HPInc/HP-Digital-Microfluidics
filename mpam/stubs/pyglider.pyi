"""Python module for interacting with Glider API"""
from __future__ import annotations
import pyglider
import typing
import os

__all__ = [
    "Board",
    "BoardId",
    "ConfigParam",
    "ConfigParamSet",
    "ESElog",
    "Electrode",
    "ErrorCode",
    "Heater",
    "Magnet",
    "Sensor"
]


class Board():
    def DisableFan(self) -> typing.Optional[ErrorCode]: 
        """
        Disable the fan
        """
    def DisableHighVoltage(self) -> typing.Optional[ErrorCode]: 
        """
        Disable high voltage
        """
    def DumpElectrodes(self) -> typing.Optional[ErrorCode]: 
        """
        Display some info about the electrodes to the console
        """
    def DumpHeaters(self) -> typing.Optional[ErrorCode]: 
        """
        Display some info about the heaters to the console
        """
    def ElectrodeAt(self, x: int, y: int) -> typing.Optional[Electrode]: 
        """
        Find the electrode (if any) at coordinate (x, y)
        """
    def ElectrodeNamed(self, name: str) -> typing.Optional[Electrode]: 
        """
        Find the electrode (if any) with the given name
        :rtype: Optional[Electrode]
        """
    def EnableFan(self) -> typing.Optional[ErrorCode]: 
        """
        Enable the fan
        """
    def EnableHighVoltage(self) -> typing.Optional[ErrorCode]: 
        """
        Enable high voltage
        """
    @staticmethod
    def Find(boardID: BoardId, *, board_rev: float, dll_dir: typing.Optional[os.PathLike] = None, config_dir: typing.Optional[os.PathLike] = None) -> Board: 
        """
        Find a board of the given type.
        """
    def GetAmbientTemperature(self) -> float: 
        """
        Get the current ambient temperature
        """
    def GetBoardColumns(self) -> int: 
        """
        Gets the number of columns for the board
        """
    def GetBoardId(self) -> BoardId: 
        """
        Gets the board id
        """
    def GetBoardRows(self) -> int: 
        """
        Gets the number of rows for the board
        """
    def GetElectrodes(self) -> typing.List[Electrode]: 
        """
        Gets a list containing each electrode object on the board
        """
    def GetHeaters(self) -> typing.List[Heater]: 
        """
        Gets a list containing each heater object on the board
        """
    def GetHighVoltage(self) -> typing.Union[float,ErrorCode]: 
        """
        Get the high voltage.  Returns a pair with the error code and the voltage.
        """
    def GetMagnets(self) -> typing.List[Magnet]: 
        """
        Gets a list containing each magnet object on the board
        """
    def GetSensors(self) -> typing.List[Sensor]: 
        """
        Gets a list containing each sensor object
        """
    def GetSupportedBoardRevisions(self) -> typing.List[float]: 
        """
        Gets a vector of supported board revisions
        """
    def HeaterNamed(self, name: str) -> typing.Optional[Heater]: 
        """
        Find the heater (if any) with the given name
        """
    def IsFanEnabled(self) -> bool: 
        """
        Is the fan enabled?
        """
    def IsHighVoltageEnabled(self) -> bool: 
        """
        Is the high voltage enaled?
        """
    def MagnetNamed(self, name: str) -> typing.Optional[Magnet]: 
        """
        Find the magnet (if any) with the given name
        """
    def MakeItSo(self) -> typing.Optional[ErrorCode]: 
        """
        Processes all outstanding requests and updates the hardware accordingly
        """
    def SetHighVoltage(self, volts: float) -> typing.Optional[ErrorCode]: 
        """
        Set the high voltage as a number of volts
        """
    def Status(self) -> typing.Optional[ErrorCode]: 
        """
        Returns the of board after initialization
        """
    def test(self) -> str: ...
    pass
class BoardId():
    """
    Enumeration of supported boards

    Members:

      Unknown

      Wallaby
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Unknown: pyglider.BoardId # value = <BoardId.Unknown: 0>
    Wallaby: pyglider.BoardId # value = <BoardId.Wallaby: 1>
    __members__: dict # value = {'Unknown': <BoardId.Unknown: 0>, 'Wallaby': <BoardId.Wallaby: 1>}
    pass
class ConfigParam():
    class ForFloat(ConfigParam):
        pass
    class ForInt(ConfigParam):
        pass
    class ForUChar(ConfigParam):
        pass
    class ForUInt(ConfigParam):
        pass
    class ForUShort(ConfigParam):
        pass
    @property
    def key(self) -> str:
        """
        :type: str
        """
    pass
class ConfigParamSet():
    @typing.overload
    def __contains__(self, cp: ConfigParam.ForFloat) -> bool: ...
    @typing.overload
    def __contains__(self, cp: ConfigParam.ForInt) -> bool: ...
    @typing.overload
    def __contains__(self, cp: ConfigParam.ForUChar) -> bool: ...
    @typing.overload
    def __contains__(self, cp: ConfigParam.ForUInt) -> bool: ...
    @typing.overload
    def __contains__(self, cp: ConfigParam.ForUShort) -> bool: ...
    @typing.overload
    def __delitem__(self, cp: ConfigParam.ForFloat) -> int: ...
    @typing.overload
    def __delitem__(self, cp: ConfigParam.ForInt) -> int: ...
    @typing.overload
    def __delitem__(self, cp: ConfigParam.ForUChar) -> int: ...
    @typing.overload
    def __delitem__(self, cp: ConfigParam.ForUInt) -> int: ...
    @typing.overload
    def __delitem__(self, cp: ConfigParam.ForUShort) -> int: ...
    @typing.overload
    def __getitem__(self, cp: ConfigParam.ForFloat) -> float: ...
    @typing.overload
    def __getitem__(self, cp: ConfigParam.ForInt) -> int: ...
    @typing.overload
    def __getitem__(self, cp: ConfigParam.ForUChar) -> int: ...
    @typing.overload
    def __getitem__(self, cp: ConfigParam.ForUInt) -> int: ...
    @typing.overload
    def __getitem__(self, cp: ConfigParam.ForUShort) -> int: ...
    @typing.overload
    def __setitem__(self, cp: ConfigParam.ForFloat, val: float) -> None: ...
    @typing.overload
    def __setitem__(self, cp: ConfigParam.ForInt, val: int) -> None: ...
    @typing.overload
    def __setitem__(self, cp: ConfigParam.ForUChar, val: int) -> None: ...
    @typing.overload
    def __setitem__(self, cp: ConfigParam.ForUInt, val: int) -> None: ...
    @typing.overload
    def __setitem__(self, cp: ConfigParam.ForUShort, val: int) -> None: ...
    @typing.overload
    def contains(self, cp: ConfigParam.ForFloat) -> bool: ...
    @typing.overload
    def contains(self, cp: ConfigParam.ForInt) -> bool: ...
    @typing.overload
    def contains(self, cp: ConfigParam.ForUChar) -> bool: ...
    @typing.overload
    def contains(self, cp: ConfigParam.ForUInt) -> bool: ...
    @typing.overload
    def contains(self, cp: ConfigParam.ForUShort) -> bool: ...
    @typing.overload
    def erase(self, cp: ConfigParam.ForFloat) -> int: ...
    @typing.overload
    def erase(self, cp: ConfigParam.ForInt) -> int: ...
    @typing.overload
    def erase(self, cp: ConfigParam.ForUChar) -> int: ...
    @typing.overload
    def erase(self, cp: ConfigParam.ForUInt) -> int: ...
    @typing.overload
    def erase(self, cp: ConfigParam.ForUShort) -> int: ...
    @typing.overload
    def find(self, cp: ConfigParam.ForFloat) -> typing.Optional[float]: ...
    @typing.overload
    def find(self, cp: ConfigParam.ForInt) -> typing.Optional[int]: ...
    @typing.overload
    def find(self, cp: ConfigParam.ForUChar) -> typing.Optional[int]: ...
    @typing.overload
    def find(self, cp: ConfigParam.ForUInt) -> typing.Optional[int]: ...
    @typing.overload
    def find(self, cp: ConfigParam.ForUShort) -> typing.Optional[int]: ...
    @typing.overload
    def set(self, cp: ConfigParam.ForFloat, val: float) -> None: ...
    @typing.overload
    def set(self, cp: ConfigParam.ForInt, val: int) -> None: ...
    @typing.overload
    def set(self, cp: ConfigParam.ForUChar, val: int) -> None: ...
    @typing.overload
    def set(self, cp: ConfigParam.ForUInt, val: int) -> None: ...
    @typing.overload
    def set(self, cp: ConfigParam.ForUShort, val: int) -> None: ...
    pass
class Sensor():
    class ResultType():
        """
        Enumeration of result types

        Members:

          Unknown

          Raw

          Millivolts
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, other: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, state: int) -> None: ...
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def value(self) -> int:
            """
            :type: int
            """
        Millivolts: pyglider.Sensor.ResultType # value = <ResultType.Millivolts: 2>
        Raw: pyglider.Sensor.ResultType # value = <ResultType.Raw: 1>
        Unknown: pyglider.Sensor.ResultType # value = <ResultType.Unknown: 0>
        __members__: dict # value = {'Unknown': <ResultType.Unknown: 0>, 'Raw': <ResultType.Raw: 1>, 'Millivolts': <ResultType.Millivolts: 2>}
        pass
    class SensorResult():
        pass
    class SensorResults():
        @property
        def results(self) -> typing.List[Sensor.SensorResult]:
            """
            :type: typing.List[Sensor.SensorResult]
            """
        pass
    class SensorType():
        """
        Enumeration of sensor types

        Members:

          Unknown

          ESElog

          ESElogEmulator
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, other: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, state: int) -> None: ...
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def value(self) -> int:
            """
            :type: int
            """
        ESElog: pyglider.Sensor.SensorType # value = <SensorType.ESElog: 1>
        ESElogEmulator: pyglider.Sensor.SensorType # value = <SensorType.ESElogEmulator: 2>
        Unknown: pyglider.Sensor.SensorType # value = <SensorType.Unknown: 0>
        __members__: dict # value = {'Unknown': <SensorType.Unknown: 0>, 'ESElog': <SensorType.ESElog: 1>, 'ESElogEmulator': <SensorType.ESElogEmulator: 2>}
        pass
    def Aim(self, bOn: bool) -> typing.Optional[ErrorCode]: 
        """
        Turn on/off an LED to assist with aiming the snsor.  Pass in True to turn On, False to turn off.
        """
    def GetConfiguration(self) -> typing.Union[ConfigParamSet,ErrorCode]: 
        """
        A copy of the current configuration, or an error.
        """
    def GetType(self) -> typing.Union[Sensor.SensorType,ErrorCode]: 
        """
        Gets the type of the sensor
        """
    def IsAvailable(self) -> typing.Union[bool,ErrorCode]: 
        """
        Returns true if the sensor is available, false if not, or an error
        """
    def IsBusy(self) -> bool: 
        """
        Returns true if the sensor is busy, false otherwise.
        """
    def ReadResultsAsync(self, units: Sensor.ResultType) -> typing.Union[Sensor.SensorResults,ErrorCode]: 
        """
        Read any available results asynchronously.  The parameter specifies raw or converted results
        """
    def ReadResultsSync(self, units: Sensor.ResultType) -> typing.Union[Sensor.SensorResults,ErrorCode]: 
        """
        Wait for any acquisition to complete and then read the results. The parameter specifies raw or converted results
        """
    @typing.overload
    def RequestSamples(self) -> typing.Union[int,ErrorCode]: 
        """
        Request samples. Returns the expected time in ms, or an error. if num_samples is omitted, uses default number.
        """
    @typing.overload
    def RequestSamples(self, num_samples: int) -> typing.Union[int,ErrorCode]: ...
    def SetConfiguration(self, sensor_config: ConfigParamSet) -> typing.Optional[ErrorCode]: ...
    pass
class Electrode():
    class ElectrodeState():
        """
        Enumeration of electrode states

        Members:

          Off

          On

          Unknown
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, other: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, state: int) -> None: ...
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def value(self) -> int:
            """
            :type: int
            """
        Off: pyglider.Electrode.ElectrodeState # value = <ElectrodeState.Off: 0>
        On: pyglider.Electrode.ElectrodeState # value = <ElectrodeState.On: 1>
        Unknown: pyglider.Electrode.ElectrodeState # value = <ElectrodeState.Unknown: 255>
        __members__: dict # value = {'Off': <ElectrodeState.Off: 0>, 'On': <ElectrodeState.On: 1>, 'Unknown': <ElectrodeState.Unknown: 255>}
        pass
    def GetCoordinatesList(self) -> typing.List[typing.Tuple[int, int]]: 
        """
        Gets the (possibly multiple) x,y coordinates of the electrode
        """
    def GetCurrentState(self) -> Electrode.ElectrodeState: 
        """
        Gets the current state of the electrode
        """
    def GetDataBufferIndex(self) -> int: 
        """
        Gets the index of the electrode in the data buffer
        """
    def GetHeaters(self) -> typing.List[str]: 
        """
        Gets the heaters associated with the electrode
        """
    def GetMagnets(self) -> typing.List[str]: 
        """
        Gets the names of magnets associated with the electrode
        """
    def GetName(self) -> str: 
        """
        Gets the name of the electrode
        """
    def GetTargetState(self) -> Electrode.ElectrodeState: 
        """
        Gets the target state of the electrode
        """
    def SetTargetState(self, electrodeState: Electrode.ElectrodeState) -> typing.Optional[ErrorCode]: 
        """
        Sets the target state of the electrode
        """
    def __repr__(self) -> str: ...
    pass
class ErrorCode():
    """
    Enumeration of error codes

    Members:

      ErrorSuccess

      ErrorFailure

      ErrorFailureHardware

      ErrorFailureToOpenFile

      ErrorFailureSystem

      ErrorHardwareNotSupported
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    ErrorFailure: pyglider.ErrorCode # value = <ErrorCode.ErrorFailure: 1>
    ErrorFailureHardware: pyglider.ErrorCode # value = <ErrorCode.ErrorFailureHardware: 2>
    ErrorFailureSystem: pyglider.ErrorCode # value = <ErrorCode.ErrorFailureSystem: 4>
    ErrorFailureToOpenFile: pyglider.ErrorCode # value = <ErrorCode.ErrorFailureToOpenFile: 3>
    ErrorHardwareNotSupported: pyglider.ErrorCode # value = <ErrorCode.ErrorHardwareNotSupported: 5>
    ErrorSuccess: pyglider.ErrorCode # value = <ErrorCode.ErrorSuccess: 0>
    __members__: dict # value = {'ErrorSuccess': <ErrorCode.ErrorSuccess: 0>, 'ErrorFailure': <ErrorCode.ErrorFailure: 1>, 'ErrorFailureHardware': <ErrorCode.ErrorFailureHardware: 2>, 'ErrorFailureToOpenFile': <ErrorCode.ErrorFailureToOpenFile: 3>, 'ErrorFailureSystem': <ErrorCode.ErrorFailureSystem: 4>, 'ErrorHardwareNotSupported': <ErrorCode.ErrorHardwareNotSupported: 5>}
    pass
class Heater():
    class HeaterState():
        """
        Enumeration of heater states

        Members:

          Off

          Heating

          Cooling

          Unknown
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, other: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, state: int) -> None: ...
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def value(self) -> int:
            """
            :type: int
            """
        Cooling: pyglider.Heater.HeaterState # value = <HeaterState.Cooling: 2>
        Heating: pyglider.Heater.HeaterState # value = <HeaterState.Heating: 1>
        Off: pyglider.Heater.HeaterState # value = <HeaterState.Off: 0>
        Unknown: pyglider.Heater.HeaterState # value = <HeaterState.Unknown: 255>
        __members__: dict # value = {'Off': <HeaterState.Off: 0>, 'Heating': <HeaterState.Heating: 1>, 'Cooling': <HeaterState.Cooling: 2>, 'Unknown': <HeaterState.Unknown: 255>}
        pass
    class HeaterStatus():
        def GetCurrentTemperature(self) -> float: 
            """
            Gets the current temperature of the heater
            """
        def GetEtaInMilliseconds(self) -> int: 
            """
            Gets the expected time in milliseconds when the current temperature will match the target temperature
            """
        def GetHeaterState(self) -> Heater.HeaterState: 
            """
            Gets the current state of the heater as a HeaterState
            """
        def GetTargetState(self) -> Heater.HeaterState: 
            """
            Gets the target state of the heater as a HeaterState
            """
        def GetTargetTemperature(self) -> float: 
            """
            Gets the target temperature of the heater
            """
        def __init__(self, hs: Heater.HeaterState, ts: Heater.HeaterState, ct: float, tt: float, etaInMs: int) -> None: ...
        pass
    class HeaterType():
        """
        Enumeration of heater types

        Members:

          Paddle

          TSR

          Peltier

          Unknown
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, other: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, state: int) -> None: ...
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def value(self) -> int:
            """
            :type: int
            """
        Paddle: pyglider.Heater.HeaterType # value = <HeaterType.Paddle: 0>
        Peltier: pyglider.Heater.HeaterType # value = <HeaterType.Peltier: 2>
        TSR: pyglider.Heater.HeaterType # value = <HeaterType.TSR: 1>
        Unknown: pyglider.Heater.HeaterType # value = <HeaterType.Unknown: 255>
        __members__: dict # value = {'Paddle': <HeaterType.Paddle: 0>, 'TSR': <HeaterType.TSR: 1>, 'Peltier': <HeaterType.Peltier: 2>, 'Unknown': <HeaterType.Unknown: 255>}
        pass
    def GetCoolingRate(self) -> float: 
        """
        Get the cooling rate in degrees C per second
        """
    def GetCurrentState(self) -> Heater.HeaterState: 
        """
        Gets the current state of the heater
        """
    def GetCurrentTemperature(self) -> float: 
        """
        Gets the current temperature of the heater
        """
    def GetElectrodeNames(self) -> typing.List[str]: 
        """
        Gets a list of names of the electrodes affected by the heater
        """
    def GetElectrodes(self) -> typing.List[Electrode]: 
        """
        Gets the electrodes affected by the heater
        """
    def GetHeatingRate(self) -> float: 
        """
        Get the heating rate in degrees C per second
        """
    def GetName(self) -> str: 
        """
        Gets the name of the heater
        """
    def GetStatus(self) -> Heater.HeaterStatus: 
        """
        Gets the status of the heater
        """
    def GetTargetState(self) -> Heater.HeaterState: 
        """
        Gets the target state of the heater
        """
    def GetTargetTemperature(self) -> float: 
        """
        Gets the target temperature of the heater
        """
    def GetType(self) -> Heater.HeaterType: 
        """
        Gets the type of the heater as a HeaterType
        """
    def SetTargetState(self, heaterState: Heater.HeaterState) -> typing.Optional[ErrorCode]: 
        """
        Sets the target state of the heater
        """
    def SetTargetTemperatureChilling(self, targetTemperature: float) -> typing.Optional[ErrorCode]: 
        """
        Sets the target temperature and turns on the chiller, or turns it off if targetTemperature is 0
        """
    def SetTargetTemperatureHeating(self, targetTemperature: float) -> typing.Optional[ErrorCode]: 
        """
        Sets the target temperature and turns on the heater, or turns it off if targetTemperature is 0
        """
    pass
class Magnet():
    class MagnetState():
        """
        Enumeration of magnet states

        Members:

          Disable

          On

          Off

          Unknown
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, other: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, state: int) -> None: ...
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def value(self) -> int:
            """
            :type: int
            """
        Disable: pyglider.Magnet.MagnetState # value = <MagnetState.Disable: 0>
        Off: pyglider.Magnet.MagnetState # value = <MagnetState.Off: 2>
        On: pyglider.Magnet.MagnetState # value = <MagnetState.On: 1>
        Unknown: pyglider.Magnet.MagnetState # value = <MagnetState.Unknown: 3>
        __members__: dict # value = {'Disable': <MagnetState.Disable: 0>, 'On': <MagnetState.On: 1>, 'Off': <MagnetState.Off: 2>, 'Unknown': <MagnetState.Unknown: 3>}
        pass
    def GetCurrentState(self) -> Magnet.MagnetState: 
        """
        Gets the current state of the magnet
        """
    def GetElectrodeNames(self) -> typing.List[str]: 
        """
        Gets a list of the names of electrodes affected by the magnet
        """
    def GetElectrods(self) -> typing.List[Electrode]: 
        """
        Gets the electrodes affected by the magnet
        """
    def GetName(self) -> str: 
        """
        Gets the name of the magnet
        """
    def GetTargetState(self) -> Magnet.MagnetState: 
        """
        Gets the target state of the magnet
        """
    def SetTargetState(self, magnetState: Magnet.MagnetState) -> typing.Optional[ErrorCode]: 
        """
        Sets the target state of the magnet
        """
    def __repr__(self) -> str: ...
    pass
class ESElog(Sensor):
    class ESElogResult(Sensor.SensorResult):
        @property
        def e1d1_valueOff(self) -> float:
            """
            :type: float
            """
        @property
        def e1d1_valueOn(self) -> float:
            """
            :type: float
            """
        @property
        def e1d2_valueOff(self) -> float:
            """
            :type: float
            """
        @property
        def e1d2_valueOn(self) -> float:
            """
            :type: float
            """
        @property
        def e2d2_valueOff(self) -> float:
            """
            :type: float
            """
        @property
        def e2d2_valueOn(self) -> float:
            """
            :type: float
            """
        @property
        def temperature(self) -> float:
            """
            :type: float
            """
        @property
        def ticket(self) -> int:
            """
            :type: int
            """
        @property
        def time(self) -> int:
            """
            :type: int
            """
        @property
        def units(self) -> Sensor.ResultType:
            """
            :type: Sensor.ResultType
            """
        pass
    ADCSamplingParam: pyglider.ConfigParam.ForUShort
    AverageParam: pyglider.ConfigParam.ForUChar
    BaudrateParam: pyglider.ConfigParam.ForUInt
    ComPortParam: pyglider.ConfigParam.ForUInt
    CycleTimeParam: pyglider.ConfigParam.ForUShort
    CyclesParam: pyglider.ConfigParam.ForUShort
    DarkSignalTypeParam: pyglider.ConfigParam.ForUInt
    E1D1FactorParam: pyglider.ConfigParam.ForFloat
    E1D1OffsetParam: pyglider.ConfigParam.ForInt
    E1D2FactorParam: pyglider.ConfigParam.ForFloat
    E1D2OffsetParam: pyglider.ConfigParam.ForInt
    E2D2FactorParam: pyglider.ConfigParam.ForFloat
    E2D2OffsetParam: pyglider.ConfigParam.ForInt
    LED1CurrentDefaultParam: pyglider.ConfigParam.ForUChar
    LED1CurrentMaxParam: pyglider.ConfigParam.ForUChar
    LED1CurrentMinParam: pyglider.ConfigParam.ForUChar
    LED1CurrentParam: pyglider.ConfigParam.ForUChar
    LED2CurrentDefaultParam: pyglider.ConfigParam.ForUChar
    LED2CurrentMaxParam: pyglider.ConfigParam.ForUChar
    LED2CurrentMinParam: pyglider.ConfigParam.ForUChar
    LED2CurrentParam: pyglider.ConfigParam.ForUChar
    LedModeParam: pyglider.ConfigParam.ForUInt
    MethodTypeParam: pyglider.ConfigParam.ForUInt
    ModbusAddressParam: pyglider.ConfigParam.ForUChar
    OffDelayLED1Param: pyglider.ConfigParam.ForUShort
    OffDelayLED2Param: pyglider.ConfigParam.ForUShort
    OnDelayLED1Param: pyglider.ConfigParam.ForUShort
    OnDelayLED2Param: pyglider.ConfigParam.ForUShort
    StartModeParam: pyglider.ConfigParam.ForUInt
    TriggerDelayParam: pyglider.ConfigParam.ForUShort
    pass
