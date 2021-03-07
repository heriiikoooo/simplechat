import signal
import sys
import ssl
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from optparse import OptionParser

clients = []
user_dict = {}
class SimpleChat(WebSocket):
   MyName = 'undefined user'
   def handleMessage(self):
      msg = self.data
      if "@" in msg:
         self.handleCommand(msg)
      else:
         for client in clients:
            if client != self:
               client.sendMessage(self.MyName +' : ' + self.data)
               

         print("broadcast")


   def handleCommand(self, commandstr):
      pos1 = commandstr.find('@')
      # print(pos1)
      pos2 = commandstr.find(' ')
      # print(pos2)
      receiver = commandstr[pos1+1:pos2]
      print('Receiver:[' + receiver + ']')
      if "server" in receiver or "Server" in receiver:
         self.handleServerCommand(commandstr[pos2+1:])
      else:
         self.handleClientCommand(commandstr[pos2+1:], receiver)


   def handleServerCommand(self, commandstr):
      # print('[' + commandstr + ']')
      pos1 = commandstr.find(' ')
      # print(pos1)
      command = commandstr[0:pos1]
      # print('[' + command + ']')
      if "setclientname"  in command:
         cname = commandstr[pos1+1:]
         print('Client name is ' + cname)
         self.MyName = cname
         self.sendMessage('@ui setclientname ' + self.MyName)
      else:
          pass
      

      #insert all the new user in dictionary
      user_dict[cname] = { 'Name': cname, 'Address': self.address, 'ServerInstance': self }
      print("-------------------------------------------------")
      print("Clients")
      print(user_dict)
      print("-------------------------------------------------")


   def handleClientCommand(self, commandstr, ReceiverName ):
      if ReceiverName in user_dict:
         print(self)
         print("Receiver  :-- " +ReceiverName)
         print(commandstr)
         server_instance = user_dict[ReceiverName]['ServerInstance']
         server_instance.sendMessage(self.MyName +"  :  "+ commandstr)
      else:
         self.sendMessage("Failed to send the message: \r\n       *** User  '"+ReceiverName+"'  did not exist!")
         print("saas \r\n user doesn't exist-----------------------")
      return self.MyName
      

   def handleConnected(self):
      print (self.address, 'connected')
      # for client in clients:
      #    client.sendMessage(self.address[0] + u' - connected')
      clients.append(self)

   def handleClose(self):
      clients.remove(self)
      print (self.address, 'closed')
      # for client in clients:
      #    client.sendMessage(self.address[0] + u' - disconnected')


class SimpleEcho(WebSocket):

   def handleMessage(self):
      self.sendMessage(self.data + '...'+ self.data)

   def handleConnected(self):
      pass

   def handleClose(self):
      pass