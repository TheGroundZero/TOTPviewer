from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadProcessor
from burp import IIntruderPayloadGenerator
import TOTPviewer as totpviewer

################################################################################
##                                                                            ##
## TOTP Viewer                                                                ##
## Provide TOTP token for Intruder sessions                                   ##
##                                                                            ##
## TOTP secret must be provided as baseValue                                  ##
##                                                                            ##
## (c) 2020 TheGroundZero / @DezeStijn                                        ##
##                                                                            ##
################################################################################


class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory, IIntruderPayloadProcessor):

	def registerExtenderCallbacks(self, callbacks):
		self._helpers = callbacks.getHelpers()
		callbacks.setExtensionName("TOTP Viewer")
		callbacks.registerIntruderPayloadGeneratorFactory(self)


	def getGeneratorName(self):
		return "TOTP Viewer"


	def createNewInstance(self, attack):
		return IntruderPayloadGenerator()


class IntruderPayloadGenerator(IIntruderPayloadGenerator):
	def __init__(self, extender, attack):
		self._extender = extender
		self._helpers = extender._helpers
		self._attack = attack
		self._payloadIndex = 0

	def hasMorePayloads(self):
		return True

	def getNextPayload(self, baseValue):
		payload = totpviewer.calc_totp(baseValue)

		print("[i] TOTP: {} ({})".format(payload, baseValue))

		self._payloadIndex += 1
		return payload

	def reset(self):
		self._payloadIndex = 0
