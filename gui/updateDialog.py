#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import wx
import bitmapLoader
import config
import service

class UpdateDialog(wx.Dialog):

    def __init__(self, parent, release):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Pyfa Update", pos = wx.DefaultPosition, size = wx.Size( 400,300 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        self.UpdateSettings = service.settings.UpdateSettings.getInstance()
        self.releaseInfo = release
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        mainSizer = wx.BoxSizer( wx.VERTICAL )
        
        headSizer = wx.BoxSizer( wx.HORIZONTAL )
        
        self.headingText = wx.StaticText( self, wx.ID_ANY, "Pyfa Update Available!", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
        self.headingText.Wrap( -1 )
        self.headingText.SetFont( wx.Font( 14, 74, 90, 92, False) )
        
        headSizer.Add( self.headingText, 1, wx.ALL, 5 )
        mainSizer.Add( headSizer, 0, wx.EXPAND, 5 )
        mainSizer.Add( wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL ), 0, wx.EXPAND |wx.ALL, 5 )
        
        versionSizer = wx.BoxSizer( wx.HORIZONTAL )

        if(self.releaseInfo['prerelease']):
            self.releaseText = wx.StaticText( self, wx.ID_ANY, "Pre-release", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
            self.releaseText.SetFont( wx.Font( 12, 74, 90, 92, False) )
            self.releaseText.SetForegroundColour( wx.Colour( 230, 0, 0 ) )
        else:       
            self.releaseText = wx.StaticText( self, wx.ID_ANY, "Stable", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
            self.releaseText.SetFont( wx.Font( 12, 74, 90, 90, False) )

        self.releaseText.Wrap( -1 )

        versionSizer.Add( self.releaseText, 1, wx.ALL, 5 )
        
        self.versionText = wx.StaticText( self, wx.ID_ANY, self.releaseInfo['tag_name'], wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.versionText.Wrap( -1 )
        self.versionText.SetFont( wx.Font( 12, 74, 90, 90, False) )
        
        versionSizer.Add( self.versionText, 1, wx.ALL, 5 )
        versionSizer.AddSpacer( ( 15, 5), 0, wx.EXPAND, 5 )
        
        mainSizer.Add( versionSizer, 0, wx.EXPAND, 5 )
        mainSizer.AddSpacer( ( 0, 5), 0, wx.EXPAND, 5 )

        notesSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.notesTextCtrl = wx.TextCtrl( self, wx.ID_ANY, self.releaseInfo['body'], wx.DefaultPosition, wx.DefaultSize, wx.TE_AUTO_URL|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_READONLY|wx.DOUBLE_BORDER|wx.TRANSPARENT_WINDOW )
        notesSizer.Add( self.notesTextCtrl, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )
        mainSizer.Add( notesSizer, 1, wx.EXPAND, 5 )
        
        self.supressCheckbox = wx.CheckBox( self, wx.ID_ANY, "Don't remind me again for this release", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.supressCheckbox.Bind(wx.EVT_CHECKBOX, self.SuppressChange)

        mainSizer.Add( self.supressCheckbox, 0, wx.ALL, 5 )
        mainSizer.Add( wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL ), 0, wx.EXPAND |wx.ALL, 5 )

        actionSizer = wx.BoxSizer( wx.HORIZONTAL )

        goSizer = wx.BoxSizer( wx.VERTICAL )
        self.goButton = wx.Button( self, wx.ID_ANY, "Download", wx.DefaultPosition, wx.DefaultSize, 0 )
        goSizer.Add( self.goButton, 0, wx.ALL, 5 )
        actionSizer.Add( goSizer, 1, wx.EXPAND, 5 )

        self.closeButton = wx.Button(self, wx.ID_CLOSE)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        actionSizer.Add( self.closeButton, 0, wx.ALL, 5 )
        mainSizer.Add( actionSizer, 0, wx.EXPAND, 5 )

        self.SetSizer( mainSizer )
        self.Layout()

        
        '''
        TODO: If release suppression is not ticked, make sure it's set correctly in settings.
        Otherwise, a release will be suppressed, and a new release will come around. However, 
        if user does not suppress that one, the old release will continue to see the suppressed 
        release in prefs
        '''
        self.Centre( wx.BOTH )

    def OnClose(self, e):
        self.Destroy()
    
    def SuppressChange(self, e):
        if (self.supressCheckbox.IsChecked()):
            self.UpdateSettings.set('version', self.releaseInfo['tag_name'])
        else:
            self.UpdateSettings.set('version', None)
