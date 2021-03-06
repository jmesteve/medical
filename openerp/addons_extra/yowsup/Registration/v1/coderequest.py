'''
Copyright (c) <2012> Tarek Galal <tare2.galal@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to the following 
conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR 
A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from ...Common.Http.warequest import WARequest
from ...Common.Http.waresponseparser import XMLResponseParser
import hashlib
from xml.dom import minidom

class WACodeRequest(WARequest):

	def __init__(self,cc, p_in, method="sms"):
		super(WACodeRequest,self).__init__();

		self.addParam("cc",cc);
		self.addParam("in",p_in);
		self.addParam("to",cc+p_in);
		self.addParam("lc","US");
		self.addParam("lg","en");
		self.addParam("mcc","000");
		self.addParam("mnc","000");
		self.addParam("imsi","000000000000000");
		self.addParam("method",method);

		self.addParam("token", self.getToken(p_in))

		self.url = "r.whatsapp.net/v1/code.php"

		self.pvars = {"status": "/code/response/@status",
					  "result": "/code/response/@result"
					}

		self.type = "POST"

		self.setParser(XMLResponseParser())

