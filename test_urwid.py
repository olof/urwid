#!/usr/bin/python
#
# Urwid unit testing .. ok, ok, ok
#    Copyright (C) 2004-2005  Ian Ward
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Urwid web site: http://excess.org/urwid/


import urwid

import unittest
from test import test_support


try: True # old python?
except: False, True = 0, 1
		

class WithinDoubleByteTest(unittest.TestCase):
	def setUp(self):
		urwid.util.set_double_byte_encoding( True )
	def wtest(self, str, ls, pos, expected, desc):
		result = urwid.util.within_double_byte(str, ls, pos)
		assert result==expected, desc+" got:"+`result`+" expected:"+`expected`
	def test1(self):
		self.wtest("mnopqr",0,2,0,'simple no high bytes')
		self.wtest("mn\xA1\xA1qr",0,2,1,'simple 1st half')
		self.wtest("mn\xA1\xA1qr",0,3,2,'simple 2nd half')
		self.wtest("m\xA1\xA1\xA1\xA1r",0,3,1,'subsequent 1st half')
		self.wtest("m\xA1\xA1\xA1\xA1r",0,4,2,'subsequent 2nd half')
		self.wtest("mn\xA1@qr",0,3,2,'simple 2nd half lo')
		self.wtest("mn\xA1\xA1@r",0,4,0,'subsequent not 2nd half lo')
		self.wtest("m\xA1\xA1\xA1@r",0,4,2,'subsequent 2nd half lo')
		
	def test2(self):
		self.wtest("\xA1\xA1qr",0,0,1,'begin 1st half')
		self.wtest("\xA1\xA1qr",0,1,2,'begin 2nd half')
		self.wtest("\xA1@qr",0,1,2,'begin 2nd half lo')
		self.wtest("\xA1\xA1\xA1\xA1r",0,2,1,'begin subs. 1st half')
		self.wtest("\xA1\xA1\xA1\xA1r",0,3,2,'begin subs. 2nd half')
		self.wtest("\xA1\xA1\xA1@r",0,3,2,'begin subs. 2nd half lo')
		self.wtest("\xA1@\xA1@r",0,3,2,'begin subs. 2nd half lo lo')
		self.wtest("@\xA1\xA1@r",0,3,0,'begin subs. not 2nd half lo')

	def test3(self):
		self.wtest("abc \xA1\xA1qr",4,4,1,'newline 1st half')
		self.wtest("abc \xA1\xA1qr",4,5,2,'newline 2nd half')
		self.wtest("abc \xA1@qr",4,5,2,'newline 2nd half lo')
		self.wtest("abc \xA1\xA1\xA1\xA1r",4,6,1,'newl subs. 1st half')
		self.wtest("abc \xA1\xA1\xA1\xA1r",4,7,2,'newl subs. 2nd half')
		self.wtest("abc \xA1\xA1\xA1@r",4,7,2,'newl subs. 2nd half lo')
		self.wtest("abc \xA1@\xA1@r",4,7,2,'newl subs. 2nd half lo lo')
		self.wtest("abc @\xA1\xA1@r",4,7,0,'newl subs. not 2nd half lo')


class CalcBreaksTest(unittest.TestCase):
	def test1(self):
		result = urwid.calculate_text_breaks( self.text,
			self.width1, self.mode )
		assert result == self.result1, result
	def test2(self):
		result = urwid.calculate_text_breaks( self.text,
			self.width2, self.mode )
		assert result == self.result2, result
	def test3(self):
		result = urwid.calculate_text_breaks( self.text,
			self.width3, self.mode )
		assert result == self.result3, result

class CalcBreaksCharTest(CalcBreaksTest):
	mode = 'any'
	text = "abfghsdjf askhtrvs\naltjhgsdf ljahtshgf"
	# tests
	width1 = 10
	result1 = [10, 19, 29]
	width2 = 6
	result2 = [6, 12, 19, 25, 31, 37]
	width3 = 100
	result3 = [19]

class CalcBreaksDBCharTest(CalcBreaksTest):
	def setUp(self):
		urwid.util.set_double_byte_encoding(True)
	mode = 'any'
	text = "abfgh\xA1\xA1j\xA1\xA1xskhtrvs\naltjhgsdf\xA1\xA1jahtshgf"
	# tests
	width1 = 10
	result1 = [10, 19, 28]
	width2 = 6
	result2 = [5, 11, 17, 19, 25, 31, 37]
	width3 = 100
	result3 = [19]

class CalcBreaksWordTest(CalcBreaksTest):
	mode = 'space'
	text = "hello world\nout there. blah"
	# tests
	width1 = 10
	result1 = [6, 12, 23]
	width2 = 5
	result2 = [6, 12, 17, 23]
	width3 = 100
	result3 = [12]

class CalcBreaksWordTest2(CalcBreaksTest):
	mode = 'space'
	text = "A simple set of words, really...."
	width1 = 10
	result1 = [9, 16, 23]
	width2 = 17
	result2 = [16]
	width3 = 13
	result3 = [13, 23]

class CalcBreaksDBWordTest(CalcBreaksTest):
	def setUp(self):
		urwid.util.set_double_byte_encoding(True)
	mode = 'space'
	text = "hel\xA1\xA1 world\nout-\xA1\xA1tre blah"
	# tests
	width1 = 10
	result1 = [6, 12, 22]
	width2 = 5
	result2 = [6, 12, 16, 22]
	width3 = 100
	result3 = [12]

class CalcTranslateTest(unittest.TestCase):
	def test_left(self):
		result = urwid.calculate_line_translation( self.text,
			self.width, self.mode, 'left')
		assert result == self.result_left, result
	def test_center(self):
		result = urwid.calculate_line_translation( self.text,
			self.width, self.mode, 'center')
		assert result == self.result_center, result
	def test_right(self):
		result = urwid.calculate_line_translation( self.text,
			self.width, self.mode, 'right')
		assert result == self.result_right, result

class CalcTranslateCharTest(CalcTranslateTest):
	text = "It's out of control!\nYou've got to"
	mode = 'any'
	width = 15
	result_left = [(0,0,0,15),(0,0,1,21),(0,0,0,34)]
	result_right = [(0,0,0,15),(10,0,1,21),(2,0,0,34)]
	result_center = [(0,0,0,15),(5,0,1,21),(1,0,0,34)]

class CalcTranslateWordTest(CalcTranslateTest):
	text = "It's out of control!\nYou've got to"
	mode = 'space'
	width = 14
	result_left = [(0,0,1,12),(0,0,1,21),(0,0,0,34)]
	result_right = [(3,0,1,12),(6,0,1,21),(1,0,0,34)]
	result_center = [(1,0,1,12),(3,0,1,21),(0,0,0,34)]

class CalcTranslateClipTest(CalcTranslateTest):
	text = "It's out of control!\nYou've got to\nturn it off!!!"
	mode = 'clip'
	width = 14
	result_left = [(0,0,7,21),(0,0,1,35),(0,0,0,49)]
	result_right = [(0,6,1,21),(1,0,1,35),(0,0,0,49)]
	result_center = [(0,3,4,21),(0,0,1,35),(0,0,0,49)]

class CalcTranslateDBClipTest(CalcTranslateTest):
	def setUp(self):
		urwid.util.set_double_byte_encoding(True)
	text = "It\xA1\xA1 \xA1\xA1t of c\xA1\xA1t\xA1\xA1l!\nYou've got to\n\xA1\xA1rn it off!\xA1\xA1"
	mode = 'clip'
	width = 14
	result_left = [(0,0,8,21),(0,0,1,35),(0,0,0,49)]
	result_right = [(1,7,1,21),(1,0,1,35),(0,0,0,49)]
	result_center = [(1,4,5,21),(0,0,1,35),(0,0,0,49)]
	


class Pos2CoordsTest(unittest.TestCase):
	sample_data = [5, 9, 20, 26]
	mytests = [
		([(0,0,0,15),(0,0,0,30)],
			[(5,0),(9,0),(5,1),(11,1)]),
		([(0,0,0,9),(0,0,0,21),(0,0,0,30)],
			[(5,0),(0,1),(11,1),(5,2)]),
		([(2,0,0,15),(2,0,0,30)], # l_pad
			[(7,0),(11,0),(7,1),(13,1)]),
		([(0,6,6,15),(0,5,5,30)], # l_trim, r_trim
			[(0,0),(3,0),(0,1),(5,1)]),
		([(0,0,0,10)],
			[(5,0),(9,0),(10,0),(10,0)]),
		
		]
		
	def test(self):
		for t, answer in self.mytests:
			r = urwid.positions_to_coords(self.sample_data, t )
			assert r==answer, "got: "+`r`+" expected: "+`answer`


class ShiftTransTest(unittest.TestCase):
	def setUp(self):
		self.trans = [(1,0,1,5),(0,1,1,12),(0,1,1,21)]
	
	def stest(self, t, expected, desc):
		assert t == expected, desc+ ". got: "+`t`+" expected: "+`expected`
	
	def testShiftTransRight(self):
		fn = urwid.shift_translation_right
		self.stest(fn(self.trans, 1, 7),
			[(2,0,1,5),(0,0,1,12),(0,0,2,21)],"right 1")
		self.stest(fn(self.trans, 2, 7),
			[(3,0,1,5),(1,0,1,12),(1,0,3,21)],"right 2")
		self.stest(fn(self.trans, 7, 7),
			[(7,0,5,5),(6,0,6,12),(6,0,8,21)],"right 7")
	
	def testShiftTransLeft(self):
		fn = urwid.shift_translation_left
		self.stest(fn(self.trans, 1, 7),
			[(0,0,1,5),(0,2,1,12),(0,2,0,21)],"left 1")
		self.stest(fn(self.trans, 2, 7),
			[(0,1,1,5),(0,3,1,12),(0,3,0,21)],"left 2")
		self.stest(fn(self.trans, 7, 7),
			[(0,5,0,5),(0,7,0,12),(0,8,0,21)],"left 7")
		



class TagMarkupTest(unittest.TestCase):
	mytests = [
		("simple one", "simple one", []),
		(('blue',"john"), "john", [('blue',4)]),
		(["a ","litt","le list"], "a little list", []),
		(["mix",('high',[" it ",('ital',"up a")])," little"],
			"mix it up a little",
			[(None,3),('high',4),('ital',4)]),
		]
	def test(self):
		for input, text, attr in self.mytests:
			restext,resattr = urwid.decompose_tagmarkup( input )
			assert restext == text, "got: "+`restext`+" expected: "+`text`
			assert resattr == attr, "got: "+`resattr`+" expected: "+`attr`
	def test_bad_tuple(self):
		try:
			urwid.decompose_tagmarkup((1,2,3))
		except urwid.TagMarkupException, e:
			pass
		else:
			assert 0, "should have thrown exception!"
		
	def test_bad_type(self):
		try:
			urwid.decompose_tagmarkup(5)
		except urwid.TagMarkupException, e:
			pass
		else:
			assert 0, "should have thrown exception!"
			


class TextTest(unittest.TestCase):
	def setUp(self):
		self.t = urwid.Text("I walk the\ncity in the night")
		
	def test_wrap(self):
		expected = ["I walk the","city in","the night"]
		got = self.t.render((10,)).text
		assert got == expected, "got: "+`got`+" expected:"+`expected`
	
	def test_left(self):
		self.t.set_align_mode('left')
		expected = ["I walk the","city in the night"]
		got = self.t.render((18,)).text
		assert got == expected, "got: "+`got`+" expected:"+`expected`
	
	def test_right(self):
		self.t.set_align_mode('right')
		expected = ["        I walk the"," city in the night"]
		got = self.t.render((18,)).text
		assert got == expected, "got: "+`got`+" expected:"+`expected`
	
	def test_center(self):
		self.t.set_align_mode('center')
		expected = ["    I walk the","city in the night"]
		got = self.t.render((18,)).text
		assert got == expected, "got: "+`got`+" expected:"+`expected`


class CalcPosTest(unittest.TestCase):
	def setUp(self):
		self.trans = [(2,0,1,8),(0,2,1,22),(3,0,0,27)]
		self.mytests = [(1,0, 0), (2,0, 0), (11,0, 7),
			(-3,1, 8), (-2,1, 8), (1,1, 11), (11,1, 21),
			(1,2, 22), (11,2, 27) ]
	
	def tests(self):
		for x,y, expected in self.mytests:
			got = urwid.calculate_pos( self.trans, x, y )
			assert got == expected, `x,y`+" got: "+`got`+" expected:"+`expected`

class EditTest(unittest.TestCase):
	def setUp(self):
		self.t1 = urwid.Edit("","blah blah")
		self.t2 = urwid.Edit("stuff:", "blah blah")
		self.t3 = urwid.Edit("junk:\n","blah blah\n\nbloo",1)
	
	def ktest(self, e, key, expected, pos, desc):
		got= e.keypress((12,),key)
		assert got == expected, desc+ ".  got: "+`got`+" expected:"+`expected`
		assert e.edit_pos == pos, desc+ ". pos: "+`e.edit_pos`+" expected pos: "+`pos`
	
	def test_left(self):
		self.t1.set_edit_pos(0)
		self.ktest(self.t1,'left','left',0,"left at left edge")
		
		self.ktest(self.t2,'left',None,8,"left within text")

		self.t3.set_edit_pos(10)
		self.ktest(self.t3,'left',None,9,"left after newline")
	
	def test_right(self):
		self.ktest(self.t1,'right','right',9,"right at right edge")
		
		self.t2.set_edit_pos(8)
		self.ktest(self.t2,'right',None,9,"right at right edge-1")
		self.t3.set_edit_pos(0)
		self.t3.keypress((12,),'right')
		assert self.t3.get_pref_col((12,)) == 1


	def test_up(self):
		self.ktest(self.t1,'up','up',9,"up at top")
		self.t2.set_edit_pos(2)
		self.t2.keypress((12,),"left")
		assert self.t2.get_pref_col((12,)) == 7
		self.ktest(self.t2,'up','up',1,"up at top again")
		assert self.t2.get_pref_col((12,)) == 7
		self.t3.set_edit_pos(10)
		self.ktest(self.t3,'up',None,0,"up at top+1")
	
	def test_down(self):
		self.ktest(self.t1,'down','down',9,"down single line")
		self.t3.set_edit_pos(5)
		self.ktest(self.t3,'down',None,10,"down line 1 to 2")
		self.ktest(self.t3,'down',None,15,"down line 2 to 3")
		self.ktest(self.t3,'down','down',15,"down at bottom")

class EditRenderTest(unittest.TestCase):
	def rtest(self, w, expected_text, expected_cursor):
		r = w.render((4,), focus = 1)
		assert r.text == expected_text, "got: "+`r.text`+" expected: "+`expected_text`
		assert r.cursor == expected_cursor, "got: "+`r.cursor`+" expected: "+`expected_cursor`

	
	def testSpaceWrap(self):
		w = urwid.Edit("","blah blah")
		w.set_edit_pos(0)
		self.rtest(w,["blah","blah"],(0,0))
		
		w.set_edit_pos(4)
		self.rtest(w,["blah","blah"],(3,0))

		w.set_edit_pos(5)
		self.rtest(w,["blah","blah"],(0,1))
		
		w.set_edit_pos(9)
		self.rtest(w,["blah","blah"],(3,1))
	
	def testClipWrap(self):
		w = urwid.Edit("","blah\nblargh",1)
		w.set_wrap_mode('clip')
		w.set_edit_pos(0)
		self.rtest(w,["blah","blar"],(0,0))
		
		w.set_edit_pos(10)
		self.rtest(w,["ah","argh"],(3,1))
		
		w.set_align_mode('right')
		w.set_edit_pos(6)
		self.rtest(w,[" bla","larg"],(0,1))
	
	def testAnyWrap(self):
		w = urwid.Edit("","blah blah")
		w.set_wrap_mode('any')
		
		self.rtest(w,["blah"," bla","h"],(1,2))


class SelectableText(urwid.Text):
	def selectable(self):
		return 1
		
	def keypress(self, size, key):
		return key
		
class ListBoxCalculateVisibleTest(unittest.TestCase):
		
	def cvtest(self, desc, body, focus, offset_rows, inset_fraction,
		exp_offset_inset, exp_cur ):
		
		lbox = urwid.ListBox(body)
		lbox.body.set_focus( focus )
		lbox.offset_rows = offset_rows
		lbox.inset_fraction = inset_fraction

		middle, top, bottom = lbox.calculate_visible((4,5),focus=1)
		offset_inset, focus_widget, focus_pos, _ign, cursor = middle
			
		if cursor is not None:
			x, y = cursor
			y += offset_inset
			cursor = x, y
				
		assert offset_inset == exp_offset_inset, "%s got: %s expected: %s" %(desc,`offset_inset`,`exp_offset_inset`)
		assert cursor == exp_cur, "%s (cursor) got: %s expected: %s" %(desc,`cursor`,`exp_cur`)
	
	def test_1simple(self):
		T = urwid.Text

		l = [T(""),T(""),T("\n"),T("\n\n"),T("\n"),T(""),T("")]

		self.cvtest( "simple top position", 
			l, 3, 0, (0,1), 0, None )		

		self.cvtest( "simple middle position", 
			l, 3, 1, (0,1), 1, None )

		self.cvtest( "simple bottom postion",
			l, 3, 2, (0,1), 2, None )

		self.cvtest( "straddle top edge",
			l, 3, 0, (1,2), -1, None )

		self.cvtest( "straddle bottom edge",
			l, 3, 4, (0,1), 4, None )

		self.cvtest( "off bottom edge",
			l, 3, 5, (0,1), 4, None )

		self.cvtest( "way off bottom edge",
			l, 3, 100, (0,1), 4, None )
	
		self.cvtest( "gap at top",
			l, 0, 2, (0,1), 0, None )
		
		self.cvtest( "gap at top and off bottom edge",
			l, 2, 5, (0,1), 2, None )

		self.cvtest( "gap at bottom",
			l, 6, 1, (0,1), 4, None )
			
		self.cvtest( "gap at bottom and straddling top edge",
			l, 4, 0, (1,2), 1, None )
			
		self.cvtest( "gap at bottom cannot completely fill",
			[T(""),T(""),T("")], 1, 0, (0,1), 1, None )
			
		self.cvtest( "gap at top and bottom",
			[T(""),T(""),T("")], 1, 2, (0,1), 1, None )

	
	def test_2cursor(self):
		T, E = urwid.Text, urwid.Edit

		l1 = [T(""),T(""),T("\n"),E("","\n\nX"),T("\n"),T(""),T("")]
		l2 = [T(""),T(""),T("\n"),E("","YY\n\n"),T("\n"),T(""),T("")]

		l2[3].set_edit_pos(2)
		
		self.cvtest( "plain cursor in view",
			l1, 3, 1, (0,1), 1, (1,3) )

		self.cvtest( "cursor off top",
			l2, 3, 0, (1,3), 0, (2, 0) )

		self.cvtest( "cursor further off top",
			l2, 3, 0, (2,3), 0, (2, 0) )

		self.cvtest( "cursor off bottom",
			l1, 3, 3, (0,1), 2, (1, 4) )

		self.cvtest( "cursor way off bottom",
			l1, 3, 100, (0,1), 2, (1, 4) )
			


class ListBoxChangeFocusTest(unittest.TestCase):
		
	def cftest(self, desc, body, pos, offset_inset, 
			coming_from, cursor, snap_rows, 
			exp_offset_rows, exp_inset_fraction, exp_cur ):
		
		lbox = urwid.ListBox(body)
		
		lbox.change_focus( (4,5), pos, offset_inset, coming_from,
			cursor, snap_rows )

		exp = exp_offset_rows, exp_inset_fraction
		act = lbox.offset_rows, lbox.inset_fraction
		
		cursor = None
		focus_widget, focus_pos = lbox.body.get_focus()
		if focus_widget.selectable():
			if hasattr(focus_widget,'get_cursor_coords'):
				cursor=focus_widget.get_cursor_coords((4,))
			
		assert act == exp, "%s got: %s expected: %s" %(desc, act, exp)
		assert cursor == exp_cur, "%s (cursor) got: %s expected: %s" %(desc,`cursor`,`exp_cur`)
	
		
	def test1unselectable(self):
		T = urwid.Text
		l = [T("\n"),T("\n\n"),T("\n\n"),T("\n\n"),T("\n")]
		
		self.cftest( "simple unselectable",
			l, 2, 0, None, None, None, 0, (0,1), None )

		self.cftest( "unselectable",
			l, 2, 1, None, None, None, 1, (0,1), None )

		self.cftest( "unselectable off top",
			l, 2, -2, None, None, None, 0, (2,3), None )
		
		self.cftest( "unselectable off bottom",
			l, 3, 2, None, None, None, 2, (0,1), None )
		
	def test2selectable(self):
		T, S = urwid.Text, SelectableText
		l = [T("\n"),T("\n\n"),S("\n\n"),T("\n\n"),T("\n")]

		self.cftest( "simple selectable",
			l, 2, 0, None, None, None, 0, (0,1), None )

		self.cftest( "selectable",
			l, 2, 1, None, None, None, 1, (0,1), None )

		self.cftest( "selectable at top",
			l, 2, 0, 'below', None, None, 0, (0,1), None )

		self.cftest( "selectable at bottom",
			l, 2, 2, 'above', None, None, 2, (0,1), None )
		
		self.cftest( "selectable off top snap",
			l, 2, -1, 'below', None, None, 0, (0,1), None )
		
		self.cftest( "selectable off bottom snap",
			l, 2, 3, 'above', None, None, 2, (0,1), None )
		
		self.cftest( "selectable off top no snap",
			l, 2, -1, 'above', None, None, 0, (1,3), None )
		
		self.cftest( "selectable off bottom no snap",
			l, 2, 3, 'below', None, None, 3, (0,1), None )
		
	def test3large_selectable(self):
		T, S = urwid.Text, SelectableText
		l = [T("\n"),S("\n\n\n\n\n\n"),T("\n")]
		self.cftest( "large selectable no snap", 
			l, 1, -1, None, None, None, 0, (1,7), None )
    
		self.cftest( "large selectable snap up", 
			l, 1, -2, 'below', None, None, 0, (0,1), None )
    
		self.cftest( "large selectable snap up2", 
			l, 1, -2, 'below', None, 2, 0, (0,1), None )
    
		self.cftest( "large selectable almost snap up", 
			l, 1, -2, 'below', None, 1, 0, (2,7), None )
    
		self.cftest( "large selectable snap down", 
			l, 1, 0, 'above', None, None, 0, (2,7), None )

		self.cftest( "large selectable snap down2", 
			l, 1, 0, 'above', None, 2, 0, (2,7), None )
			
		self.cftest( "large selectable almost snap down", 
			l, 1, 0, 'above', None, 1, 0, (0,1), None )
	
	def test4cursor(self):
		T,E = urwid.Text, urwid.Edit
		#...
			
		
		
class ListBoxRenderTest(unittest.TestCase):
		
	def ltest(self,desc,body,focus,offset_inset_rows,exp_text,exp_cur):
		
		lbox = urwid.ListBox(body)
		lbox.body.set_focus( focus )
		lbox.shift_focus((4,10), offset_inset_rows )
		canvas = lbox.render( (4,5), focus=1 )

		text = canvas.text
		cursor = canvas.cursor
		
		assert text == exp_text, "%s (text) got: %s expected: %s" %(desc,`text`,`exp_text`)
		assert cursor == exp_cur, "%s (cursor) got: %s expected: %s" %(desc,`cursor`,`exp_cur`)
		
	
	def test1Simple(self):
		T = urwid.Text
		
		self.ltest( "simple one text item render",
			[T("1\n2")], 0, 0,
			["1","2","","",""],None)

		self.ltest( "simple multi text item render off bottom",
			[T("1"),T("2"),T("3\n4"),T("5"),T("6")], 2, 2,
			["1","2","3","4","5"],None)

		self.ltest( "simple multi text item render off top",
			[T("1"),T("2"),T("3\n4"),T("5"),T("6")], 2, 1,
			["2","3","4","5","6"],None)

	def test2Trim(self):
		T = urwid.Text
		
		self.ltest( "trim unfocused bottom",
			[T("1\n2"),T("3\n4"),T("5\n6")], 1, 2,
			["1","2","3","4","5"],None)
		
		self.ltest( "trim unfocused top",
			[T("1\n2"),T("3\n4"),T("5\n6")], 1, 1,
			["2","3","4","5","6"],None)
		
		self.ltest( "trim none full focus",
			[T("1\n2\n3\n4\n5")], 0, 0,
			["1","2","3","4","5"],None)
		
		self.ltest( "trim focus bottom",
			[T("1\n2\n3\n4\n5\n6")], 0, 0,
			["1","2","3","4","5"],None)
		
		self.ltest( "trim focus top",
			[T("1\n2\n3\n4\n5\n6")], 0, -1,
			["2","3","4","5","6"],None)
		
		self.ltest( "trim focus top and bottom",
			[T("1\n2\n3\n4\n5\n6\n7")], 0, -1,
			["2","3","4","5","6"],None)
		
	def test3Shift(self):
		T,E = urwid.Text, urwid.Edit
		
		self.ltest( "shift up one fit",
			[T("1\n2"),T("3"),T("4"),T("5"),T("6")], 4, 5,
			["2","3","4","5","6"],None)
			
		e = E("","ab\nc",1)
		e.set_edit_pos( 2 )
		self.ltest( "shift down one cursor over edge",
			[e,T("3"),T("4"),T("5\n6")], 0, -1,
			["ab","c","3","4","5"], (2,0))
			
		self.ltest( "shift up one cursor over edge",
			[T("1\n2"),T("3"),T("4"),E("","d\ne")], 3, 4,
			["2","3","4","d","e"], (1,4))

		self.ltest( "shift none cursor top focus over edge",
			[E("","ab\n"),T("3"),T("4"),T("5\n6")], 0, -1,
			["","3","4","5","6"], (0,0))

		e = E("","abc\nd")
		e.set_edit_pos( 3 )
		self.ltest( "shift none cursor bottom focus over edge",
			[T("1\n2"),T("3"),T("4"),e], 3, 4,
			["1","2","3","4","abc"], (3,4))
			
		
class ListBoxKeypressTest(unittest.TestCase):
		
	def ktest(self, desc, key, body, focus, offset_inset,
		exp_focus, exp_offset_inset, exp_cur, lbox = None):
		
		if lbox is None:
			lbox = urwid.ListBox(body)
			lbox.body.set_focus( focus )
			lbox.shift_focus((4,10), offset_inset )

		ret_key = lbox.keypress((4,5),key)
		middle, top, bottom = lbox.calculate_visible((4,5),focus=1)
		offset_inset, focus_widget, focus_pos, _ign, cursor = middle
			
		if cursor is not None:
			x, y = cursor
			y += offset_inset
			cursor = x, y
				
		exp = exp_focus, exp_offset_inset
		act = focus_pos, offset_inset
		assert act == exp, "%s got: %s expected: %s" %(desc,`act`,`exp`)
		assert cursor == exp_cur, "%s (cursor) got: %s expected: %s" %(desc,`cursor`,`exp_cur`)
		return ret_key,lbox
		
		
	def test1_up(self):
		T,S,E = urwid.Text, SelectableText, urwid.Edit
		
		self.ktest( "direct selectable both visible", 'up',
			[S(""),S("")], 1, 1,
			0, 0, None )

		self.ktest( "selectable skip one all visible", 'up',
			[S(""),T(""),S("")], 2, 2,
			0, 0, None )

		key,lbox = self.ktest( "nothing above no scroll", 'up',
			[S("")], 0, 0,
			0, 0, None )
		assert key == 'up'

		key, lbox = self.ktest( "unselectable above no scroll", 'up',
			[T(""),T(""),S("")], 2, 2,
			2, 2, None )
		assert key == 'up'

		self.ktest( "unselectable above scroll 1", 'up',
			[T(""),S(""),T("\n\n\n")], 1, 0,
			1, 1, None )

		self.ktest( "selectable above scroll 1", 'up',
			[S(""),S(""),T("\n\n\n")], 1, 0,
			0, 0, None )

		self.ktest( "selectable above too far", 'up',
			[S(""),T(""),S(""),T("\n\n\n")], 2, 0,
			2, 1, None )

		self.ktest( "selectable above skip 1 scroll 1", 'up',
			[S(""),T(""),S(""),T("\n\n\n")], 2, 1,
			0, 0, None )

		self.ktest( "tall selectable above scroll 2", 'up',
			[S(""),S("\n"),S(""),T("\n\n\n")], 2, 0,
			1, 0, None )

		self.ktest( "very tall selectable above scroll 5", 'up',
			[S(""),S("\n\n\n\n"),S(""),T("\n\n\n\n")], 2, 0,
			1, 0, None )

		self.ktest( "very tall selected scroll within 1", 'up',
			[S(""),S("\n\n\n\n\n")], 1, -1,
			1, 0, None )

		self.ktest( "edit above pass cursor", 'up',
			[E("","abc"),E("","de")], 1, 1,
			0, 0, (2, 0) )

		key,lbox = self.ktest( "edit too far above pass cursor A", 'up',
			[E("","abc"),T("\n\n\n\n"),E("","de")], 2, 4,
			1, 0, None )

		self.ktest( "edit too far above pass cursor B", 'up',
			None, None, None,
			0, 0, (2,0), lbox )

		self.ktest( "within focus cursor made not visible", 'up',
			[T("\n\n\n"),E("hi\n","ab")], 1, 3,
			0, 0, None )

		self.ktest( "within focus cursor made not visible (2)", 'up',
			[T("\n\n\n\n"),E("hi\n","ab")], 1, 3,
			0, -1, None )
		
		self.ktest( "force focus unselectable" , 'up',
			[T("\n\n\n\n"),S("")], 1, 4,
			0, 0, None )
		
		self.ktest( "pathological cursor widget", 'up',
			[T("\n"),E("\n\n\n\n\n","a")], 1, 4,
			0, -1, None )
		
		self.ktest( "unselectable to unselectable", 'up',
			[T(""),T(""),T(""),T(""),T(""),T(""),T("")], 2, 0,
			1, 0, None )

		self.ktest( "unselectable over edge to same", 'up',
			[T(""),T("12\n34"),T(""),T(""),T(""),T("")],1,-1,
			1, 0, None )
		
		key,lbox = self.ktest( "edit short between pass cursor A", 'up',
			[E("","abcd"),E("","a"),E("","def")], 2, 2,
			1, 1, (1,1) )

		self.ktest( "edit short between pass cursor B", 'up',
			None, None, None,
			0, 0, (3,0), lbox )

	def test2_down(self):	
		T,S,E = urwid.Text, SelectableText, urwid.Edit
		
		self.ktest( "direct selectable both visible", 'down',
			[S(""),S("")], 0, 0,
			1, 1, None )

		self.ktest( "selectable skip one all visible", 'down',
			[S(""),T(""),S("")], 0, 0,
			2, 2, None )

		key,lbox = self.ktest( "nothing below no scroll", 'down',
			[S("")], 0, 0,
			0, 0, None )
		assert key == 'down'

		key, lbox = self.ktest( "unselectable below no scroll", 'down',
			[S(""),T(""),T("")], 0, 0,
			0, 0, None )
		assert key == 'down'

		self.ktest( "unselectable below scroll 1", 'down',
			[T("\n\n\n"),S(""),T("")], 1, 4,
			1, 3, None )

		self.ktest( "selectable below scroll 1", 'down',
			[T("\n\n\n"),S(""),S("")], 1, 4,
			2, 4, None )

		self.ktest( "selectable below too far", 'down',
			[T("\n\n\n"),S(""),T(""),S("")], 1, 4,
			1, 3, None )

		self.ktest( "selectable below skip 1 scroll 1", 'down',
			[T("\n\n\n"),S(""),T(""),S("")], 1, 3,
			3, 4, None )

		self.ktest( "tall selectable below scroll 2", 'down',
			[T("\n\n\n"),S(""),S("\n"),S("")], 1, 4,
			2, 3, None )

		self.ktest( "very tall selectable below scroll 5", 'down',
			[T("\n\n\n\n"),S(""),S("\n\n\n\n"),S("")], 1, 4,
			2, 0, None )

		self.ktest( "very tall selected scroll within 1", 'down',
			[S("\n\n\n\n\n"),S("")], 0, 0,
			0, -1, None )

		self.ktest( "edit below pass cursor", 'down',
			[E("","de"),E("","abc")], 0, 0,
			1, 1, (2, 1) )

		key,lbox=self.ktest( "edit too far below pass cursor A", 'down',
			[E("","de"),T("\n\n\n\n"),E("","abc")], 0, 0,
			1, 0, None )

		self.ktest( "edit too far below pass cursor B", 'down',
			None, None, None,
			2, 4, (2,4), lbox )

		odd_e = E("","hi\nab")
		odd_e.set_edit_pos( 2 )
		# disble cursor movement in odd_e object
		odd_e.move_cursor_to_coords = lambda s,c,xy: 0
		self.ktest( "within focus cursor made not visible", 'down',
			[odd_e,T("\n\n\n\n")], 0, 0,
			1, 1, None )

		self.ktest( "within focus cursor made not visible (2)", 'down',
			[odd_e,T("\n\n\n\n"),], 0, 0,
			1, 1, None )
		
		self.ktest( "force focus unselectable" , 'down',
			[S(""),T("\n\n\n\n")], 0, 0,
			1, 0, None )
		
		odd_e.set_edit_text( "hi\n\n\n\n\n" )
		self.ktest( "pathological cursor widget", 'down',
			[odd_e,T("\n")], 0, 0,
			1, 4, None )

		self.ktest( "unselectable to unselectable", 'down',
			[T(""),T(""),T(""),T(""),T(""),T(""),T("")], 4, 4,
			5, 4, None )

		self.ktest( "unselectable over edge to same", 'down',
			[T(""),T(""),T(""),T(""),T("12\n34"),T("")],4,4,
			4, 3, None )
		
		key,lbox=self.ktest( "edit short between pass cursor A", 'down',
			[E("","abc"),E("","a"),E("","defg")], 0, 0,
			1, 1, (1,1) )

		self.ktest( "edit short between pass cursor B", 'down',
			None, None, None,
			2, 2, (3,2), lbox )
			
	def test3_page_up(self):
		T,S,E = urwid.Text, SelectableText, urwid.Edit
		
		self.ktest( "unselectable aligned to aligned", 'page up',
			[T(""),T("\n"),T("\n\n"),T(""),T("\n"),T("\n\n")], 3, 0,
			1, 0, None )

		self.ktest( "unselectable unaligned to aligned", 'page up',
			[T(""),T("\n"),T("\n"),T("\n"),T("\n"),T("\n\n")], 3,-1,
			1, 0, None )
			
		self.ktest( "selectable to unselectable", 'page up',
			[T(""),T("\n"),T("\n"),T("\n"),S("\n"),T("\n\n")], 4, 1,
			1, -1, None )
			
		self.ktest( "selectable to cut off selectable", 'page up',
			[S("\n\n"),T("\n"),T("\n"),S("\n"),T("\n\n")], 3, 1,
			0, -2, None )
			
		self.ktest( "seletable to selectable", 'page up',
			[T("\n\n"),S("\n"),T("\n"),S("\n"),T("\n\n")], 3, 1,
			1, 1, None )

		self.ktest( "within very long selectable", 'page up',
			[S(""),S("\n\n\n\n\n\n\n\n"),T("\n")], 1, -6,
			1, -1, None )

		e = E("","\n\nab\n\n\n\n\ncd\n")
		e.set_edit_pos(11)
		self.ktest( "within very long cursor widget", 'page up',
			[S(""),e,T("\n")], 1, -6,
			1, -2, (2, 0) )

		self.ktest( "pathological cursor widget", 'page up',
			[T(""),E("\n\n\n\n\n\n\n\n","ab"),T("")], 1, -5,
			0, 0, None )

		e = E("","\nab\n\n\n\n\ncd\n")
		e.set_edit_pos(10)
		self.ktest( "very long cursor widget snap", 'page up',
			[T(""),e,T("\n")], 1, -5, 
			1, 0, (2, 1) )

		self.ktest( "slight scroll selectable", 'page up',
			[T("\n"),S("\n"),T(""),S(""),T("\n\n\n"),S("")], 5, 4,
			3, 0, None )

		self.ktest( "scroll into snap region", 'page up',
			[T("\n"),S("\n"),T(""),T(""),T("\n\n\n"),S("")], 5, 4,
			1, 0, None )

		self.ktest( "mid scroll short", 'page up',
			[T("\n"),T(""),T(""),S(""),T(""),T("\n"),S(""),T("\n")],
			6, 2,	3, 1, None )

		self.ktest( "mid scroll long", 'page up',
			[T("\n"),S(""),T(""),S(""),T(""),T("\n"),S(""),T("\n")],
			6, 2,	1, 0, None )

		self.ktest( "mid scroll perfect", 'page up',
			[T("\n"),S(""),S(""),S(""),T(""),T("\n"),S(""),T("\n")],
			6, 2,	2, 0, None )

		self.ktest( "cursor move up fail short", 'page up',
			[T("\n"),T("\n"),E("","\nab"),T(""),T("")], 2, 1,
			2, 4, (0, 4) )

		self.ktest( "cursor force fail short", 'page up',
			[T("\n"),T("\n"),E("\n","ab"),T(""),T("")], 2, 1,
			0, 0, None )

		odd_e = E("","hi\nab")
		odd_e.set_edit_pos( 2 )
		# disble cursor movement in odd_e object
		odd_e.move_cursor_to_coords = lambda s,c,xy: 0
		self.ktest( "cursor force fail long", 'page up',
			[odd_e,T("\n"),T("\n"),T("\n"),S(""),T("\n")], 4, 2,
			1, -1, None )

		self.ktest( "prefer not cut off", 'page up',
			[S("\n"),T("\n"),S(""),T("\n\n"),S(""),T("\n")], 4, 2,
			2, 1, None )

		self.ktest( "allow cut off", 'page up',
			[S("\n"),T("\n"),T(""),T("\n\n"),S(""),T("\n")], 4, 2,
			0, -1, None )

		self.ktest( "at top fail", 'page up',
			[T("\n\n"),T("\n"),T("\n\n\n")], 0, 0,
			0, 0, None )
		
		self.ktest( "all visible fail", 'page up',
			[T("a"),T("\n")], 0, 0,
			0, 0, None )

		self.ktest( "current ok fail", 'page up',
			[T("\n\n"),S("hi")], 1, 3,
			1, 3, None )

		self.ktest( "all visible choose top selectable", 'page up',
			[T(""),S("a"),S("b"),S("c")], 3, 3,
			1, 1, None )

		self.ktest( "bring in edge choose top", 'page up',
			[S("b"),T("-"),S("-"),T("c"),S("d"),T("-")],4,3,
			0, 0, None )
		
		self.ktest( "bring in edge choose top selectable", 'page up',
			[T("b"),S("-"),S("-"),T("c"),S("d"),T("-")],4,3,
			1, 1, None )
		
	def test4_page_down(self):
		T,S,E = urwid.Text, SelectableText, urwid.Edit
		
		self.ktest( "unselectable aligned to aligned", 'page down',
			[T("\n\n"),T("\n"),T(""),T("\n\n"),T("\n"),T("")], 2, 4,
			4, 3, None )

		self.ktest( "unselectable unaligned to aligned", 'page down',
			[T("\n\n"),T("\n"),T("\n"),T("\n"),T("\n"),T("")], 2, 4,
			4, 3, None )
			
		self.ktest( "selectable to unselectable", 'page down',
			[T("\n\n"),S("\n"),T("\n"),T("\n"),T("\n"),T("")], 1, 2,
			4, 4, None )
			
		self.ktest( "selectable to cut off selectable", 'page down',
			[T("\n\n"),S("\n"),T("\n"),T("\n"),S("\n\n")], 1, 2,
			4, 4, None )
			
		self.ktest( "seletable to selectable", 'page down',
			[T("\n\n"),S("\n"),T("\n"),S("\n"),T("\n\n")], 1, 1,
			3, 2, None )

		self.ktest( "within very long selectable", 'page down',
			[T("\n"),S("\n\n\n\n\n\n\n\n"),S("")], 1, 2,
			1, -3, None )

		e = E("","\nab\n\n\n\n\ncd\n\n")
		e.set_edit_pos(2)
		self.ktest( "within very long cursor widget", 'page down',
			[T("\n"),e,S("")], 1, 2,
			1, -2, (1, 4) )

		odd_e = E("","ab\n\n\n\n\n\n\n\n\n")
		odd_e.set_edit_pos( 1 )
		# disble cursor movement in odd_e object
		odd_e.move_cursor_to_coords = lambda s,c,xy: 0
		self.ktest( "pathological cursor widget", 'page down',
			[T(""),odd_e,T("")], 1, 1,
			2, 4, None )

		e = E("","\nab\n\n\n\n\ncd\n")
		e.set_edit_pos(2)
		self.ktest( "very long cursor widget snap", 'page down',
			[T("\n"),e,T("")], 1, 2, 
			1, -3, (1, 3) )

		self.ktest( "slight scroll selectable", 'page down',
			[S(""),T("\n\n\n"),S(""),T(""),S("\n"),T("\n")], 0, 0,
			2, 4, None )

		self.ktest( "scroll into snap region", 'page down',
			[S(""),T("\n\n\n"),T(""),T(""),S("\n"),T("\n")], 0, 0,
			4, 3, None )

		self.ktest( "mid scroll short", 'page down',
			[T("\n"),S(""),T("\n"),T(""),S(""),T(""),T(""),T("\n")],
			1, 2,	4, 3, None )

		self.ktest( "mid scroll long", 'page down',
			[T("\n"),S(""),T("\n"),T(""),S(""),T(""),S(""),T("\n")],
			1, 2,	6, 4, None )

		self.ktest( "mid scroll perfect", 'page down',
			[T("\n"),S(""),T("\n"),T(""),S(""),S(""),S(""),T("\n")],
			1, 2,	5, 4, None )

		e = E("","hi\nab")
		e.set_edit_pos( 1 )
		self.ktest( "cursor move up fail short", 'page down',
			[T(""),T(""),e,T("\n"),T("\n")], 2, 1,
			2, -1, (1, 0) )


		odd_e = E("","hi\nab")
		odd_e.set_edit_pos( 1 )
		# disble cursor movement in odd_e object
		odd_e.move_cursor_to_coords = lambda s,c,xy: 0
		self.ktest( "cursor force fail short", 'page down',
			[T(""),T(""),odd_e,T("\n"),T("\n")], 2, 2, 
			4, 3, None )

		self.ktest( "cursor force fail long", 'page down',
			[T("\n"),S(""),T("\n"),T("\n"),T("\n"),E("hi\n","ab")],
			1, 2,	4, 4, None )
			
		self.ktest( "prefer not cut off", 'page down',
			[T("\n"),S(""),T("\n\n"),S(""),T("\n"),S("\n")], 1, 2,
			3, 3, None )
			
		self.ktest( "allow cut off", 'page down',
			[T("\n"),S(""),T("\n\n"),T(""),T("\n"),S("\n")], 1, 2,
			5, 4, None )
		
		self.ktest( "at bottom fail", 'page down',
			[T("\n\n"),T("\n"),T("\n\n\n")], 2, 1,
			2, 1, None )

		self.ktest( "all visible fail", 'page down',
			[T("a"),T("\n")], 1, 1,
			1, 1, None )

		self.ktest( "current ok fail", 'page down',
			[S("hi"),T("\n\n")], 0, 0,
			0, 0, None )

		self.ktest( "all visible choose last selectable", 'page down',
			[S("a"),S("b"),S("c"),T("")], 0, 0,
			2, 2, None )
		
		self.ktest( "bring in edge choose last", 'page down',
			[T("-"),S("d"),T("c"),S("-"),T("-"),S("b")],1,1,
			5,4, None )
		
		self.ktest( "bring in edge choose last selectable", 'page down',
			[T("-"),S("d"),T("c"),S("-"),S("-"),T("b")],1,1,
			4,3, None )
		

class PaddingTest(unittest.TestCase):
	def ptest(self, desc, align, width, maxcol, left, right,min_width=None):
		p = urwid.Padding(None, align, width, min_width)
		l, r = p.padding_values((maxcol,))
		assert (l,r)==(left,right), "%s expected %s but got %s"%(
			desc, (left,right), (l,r))
	
	def petest(self, desc, align, width):
		try:
			urwid.Padding(None, align, width)
		except urwid.PaddingError, e:
			return	
		assert 0, "%s expected error!" % desc
		
	def test_create(self):
		self.petest("invalid pad",6,5)
		self.petest("invalid pad type",('bad',2),5)
		self.petest("invalid width",'center','42')
		self.petest("invalid width type",'center',('gouranga',4))
		self.petest("invalid combination",('relative',20),
			('fixed right',4))
		self.petest("invalid combination 2",('relative',20),
			('fixed left',4))
		
	def test_values(self):	
		self.ptest("left align 5 7",'left',5,7,0,2)
		self.ptest("left align 7 7",'left',7,7,0,0)
		self.ptest("left align 9 7",'left',9,7,0,0)
		self.ptest("right align 5 7",'right',5,7,2,0)
		self.ptest("center align 5 7",'center',5,7,1,1)
		self.ptest("fixed left",('fixed left',3),5,10,3,2)
		self.ptest("fixed left reduce",('fixed left',3),8,10,2,0)
		self.ptest("fixed left shrink",('fixed left',3),18,10,0,0)
		self.ptest("fixed left, right",
			('fixed left',3),('fixed right',4),17,3,4)
		self.ptest("fixed left, right, min_width",
			('fixed left',3),('fixed right',4),10,3,2,5)
		self.ptest("fixed left, right, min_width 2",
			('fixed left',3),('fixed right',4),10,2,0,8)
		self.ptest("fixed right",('fixed right',3),5,10,2,3)
		self.ptest("fixed right reduce",('fixed right',3),8,10,0,2)
		self.ptest("fixed right shrink",('fixed right',3),18,10,0,0)
		self.ptest("fixed right, left",
			('fixed right',3),('fixed left',4),17,4,3)
		self.ptest("fixed right, left, min_width",
			('fixed right',3),('fixed left',4),10,2,3,5)
		self.ptest("fixed right, left, min_width 2",
			('fixed right',3),('fixed left',4),10,0,2,8)
		self.ptest("relative 30",('relative',30),5,10,1,4)
		self.ptest("relative 50",('relative',50),5,10,2,3)
		self.ptest("relative 130 edge",('relative',130),5,10,5,0)
		self.ptest("relative -10 edge",('relative',-10),4,10,0,6)
		self.ptest("center relative 70",'center',('relative',70),
			10,1,2)
		self.ptest("center relative 70 grow 8",'center',('relative',70),
			10,1,1,8)

	def mctest(self, desc, left, right, size, cx, innercx):
		class Inner:
			def __init__(self, desc, innercx):
				self.desc = desc
				self.innercx = innercx
			def move_cursor_to_coords(self,size,cx,cy):
				assert cx==self.innercx, desc
		i = Inner(desc,innercx)
		p = urwid.Padding(i, ('fixed left',left),
			('fixed right',right))
		p.move_cursor_to_coords(size, cx, 0)

	def test_cursor(self):
		self.mctest("cursor left edge",2,2,(10,2),2,0) 
		self.mctest("cursor left edge-1",2,2,(10,2),1,0) 
		self.mctest("cursor right edge",2,2,(10,2),7,5)
		self.mctest("cursor right edge+1",2,2,(10,2),8,5) 



class FillerTest(unittest.TestCase):
	def ftest(self, desc, valign, height, maxrow, top, bottom, 
			min_height=None):
		f = urwid.Filler(None, valign, height, min_height)
		t, b = f.filler_values((20,maxrow), False)
		assert (t,b)==(top,bottom), "%s expected %s but got %s"%(
			desc, (top,bottom), (t,b))
	
	def fetest(self, desc, valign, height):
		try:
			urwid.Filler(None, valign, height)
		except urwid.FillerError, e:
			return	
		assert 0, "%s expected error!" % desc
		
	def test_create(self):
		self.fetest("invalid pad",6,5)
		self.fetest("invalid pad type",('bad',2),5)
		self.fetest("invalid width",'middle','42')
		self.fetest("invalid width type",'middle',('gouranga',4))
		self.fetest("invalid combination",('relative',20),
			('fixed bottom',4))
		self.fetest("invalid combination 2",('relative',20),
			('fixed top',4))
		
	def test_values(self):	
		self.ftest("top align 5 7",'top',5,7,0,2)
		self.ftest("top align 7 7",'top',7,7,0,0)
		self.ftest("top align 9 7",'top',9,7,0,0)
		self.ftest("bottom align 5 7",'bottom',5,7,2,0)
		self.ftest("middle align 5 7",'middle',5,7,1,1)
		self.ftest("fixed top",('fixed top',3),5,10,3,2)
		self.ftest("fixed top reduce",('fixed top',3),8,10,2,0)
		self.ftest("fixed top shrink",('fixed top',3),18,10,0,0)
		self.ftest("fixed top, bottom",
			('fixed top',3),('fixed bottom',4),17,3,4)
		self.ftest("fixed top, bottom, min_width",
			('fixed top',3),('fixed bottom',4),10,3,2,5)
		self.ftest("fixed top, bottom, min_width 2",
			('fixed top',3),('fixed bottom',4),10,2,0,8)
		self.ftest("fixed bottom",('fixed bottom',3),5,10,2,3)
		self.ftest("fixed bottom reduce",('fixed bottom',3),8,10,0,2)
		self.ftest("fixed bottom shrink",('fixed bottom',3),18,10,0,0)
		self.ftest("fixed bottom, top",
			('fixed bottom',3),('fixed top',4),17,4,3)
		self.ftest("fixed bottom, top, min_height",
			('fixed bottom',3),('fixed top',4),10,2,3,5)
		self.ftest("fixed bottom, top, min_height 2",
			('fixed bottom',3),('fixed top',4),10,0,2,8)
		self.ftest("relative 30",('relative',30),5,10,1,4)
		self.ftest("relative 50",('relative',50),5,10,2,3)
		self.ftest("relative 130 edge",('relative',130),5,10,5,0)
		self.ftest("relative -10 edge",('relative',-10),4,10,0,6)
		self.ftest("middle relative 70",'middle',('relative',70),
			10,1,2)
		self.ftest("middle relative 70 grow 8",'middle',('relative',70),
			10,1,1,8)


class FrameTest(unittest.TestCase):

	def ftbtest(self, desc, focus_part, header_rows, footer_rows, size, 
			focus, top, bottom):
		class FakeWidget:
			def __init__(self, rows, want_focus):
				self.ret_rows = rows
				self.want_focus = want_focus
			def rows(self, size, focus=False):
				assert self.want_focus == focus
				return self.ret_rows
		header = footer = None
		if header_rows:
			header = FakeWidget(header_rows, 
				focus and focus_part == 'header')
		if footer_rows:
			footer = FakeWidget(footer_rows,
				focus and focus_part == 'footer')
				
		f = urwid.Frame(None, header, footer, focus_part)

		rval = f.frame_top_bottom(size, focus)
		exp = (top, bottom), (header_rows, footer_rows)
		assert exp == rval, "%s expected %s but got %s"%(
			desc,`exp`,`rval`)
		
	def test(self):
		self.ftbtest("simple", 'body', 0, 0, (9, 10), True, 0, 0)
		self.ftbtest("simple h", 'body', 3, 0, (9, 10), True, 3, 0)
		self.ftbtest("simple f", 'body', 0, 3, (9, 10), True, 0, 3)
		self.ftbtest("simple hf", 'body', 3, 3, (9, 10), True, 3, 3)
		self.ftbtest("almost full hf", 'body', 4, 5, (9, 10), 
			True, 4, 5)
		self.ftbtest("full hf", 'body', 5, 5, (9, 10), 
			True, 4, 5)
		self.ftbtest("x full h+1f", 'body', 6, 5, (9, 10), 
			False, 4, 5)
		self.ftbtest("full h+1f", 'body', 6, 5, (9, 10), 
			True, 4, 5)
		self.ftbtest("full hf+1", 'body', 5, 6, (9, 10), 
			True, 3, 6)
		self.ftbtest("F full h+1f", 'footer', 6, 5, (9, 10), 
			True, 5, 5)
		self.ftbtest("F full hf+1", 'footer', 5, 6, (9, 10), 
			True, 4, 6)
		self.ftbtest("F full hf+5", 'footer', 5, 11, (9, 10), 
			True, 0, 10)
		self.ftbtest("full hf+5", 'body', 5, 11, (9, 10), 
			True, 0, 9)
		self.ftbtest("H full hf+1", 'header', 5, 6, (9, 10), 
			True, 5, 5)
		self.ftbtest("H full h+1f", 'header', 6, 5, (9, 10), 
			True, 6, 4)
		self.ftbtest("H full h+5f", 'header', 11, 5, (9, 10), 
			True, 10, 0)


class PileTest(unittest.TestCase):
	def ktest(self, desc, l, focus_item, key, 
			rkey, rfocus, rpref_col):
		p = urwid.Pile( l, focus_item )
		rval = p.keypress( (20,), key )
		assert rkey == rval, "%s key expected %s but got %s" %(
			desc, `rkey`, `rval`)
		new_focus = l.index(p.get_focus())
		assert new_focus == rfocus, "%s focus expected %s but got %s" %(
			desc, `rfocus`, `new_focus`)
		new_pref = p.get_pref_col((20,))
		assert new_pref == rpref_col, (
			"%s pref_col expected %s but got %s" % (
			desc, `rpref_col`, `new_pref`))
	
	def test_select_change(self):
		T,S,E = urwid.Text, SelectableText, urwid.Edit

		self.ktest("simple up", [S("")], 0, "up", "up", 0, None)
		self.ktest("simple down", [S("")], 0, "down", "down", 0, None)
		self.ktest("ignore up", [T(""),S("")], 1, "up", "up", 1, None)
		self.ktest("ignore down", [S(""),T("")], 0, "down", 
			"down", 0, None)
		self.ktest("step up", [S(""),S("")], 1, "up", None, 0, None)
		self.ktest("step down", [S(""),S("")], 0, "down", 
			None, 1, None)
		self.ktest("skip step up", [S(""),T(""),S("")], 2, "up", 
			None, 0, None)
		self.ktest("skip step down", [S(""),T(""),S("")], 0, "down", 
			None, 2, None)
		self.ktest("pad skip step up", [T(""),S(""),T(""),S("")], 3, 
			"up", None, 1, None)
		self.ktest("pad skip step down", [S(""),T(""),S(""),T("")], 0, 
			"down", None, 2, None)
		self.ktest("padi skip step up", [S(""),T(""),S(""),T(""),S("")],
			4, "up", None, 2, None)
		self.ktest("padi skip step down", [S(""),T(""),S(""),T(""),
			S("")], 0, "down", None, 2, None)
		e = E("","abcd", edit_pos=1)
		e.keypress((20,),"right") # set a pref_col
		self.ktest("pref step up", [S(""),T(""),e], 2, "up", 
			None, 0, 2)
		self.ktest("pref step down", [e,T(""),S("")], 0, "down", 
			None, 2, 2)
		z = E("","1234")
		self.ktest("prefx step up", [z,T(""),e], 2, "up", 
			None, 0, 2)
		assert z.get_pref_col((20,)) == 2
		z = E("","1234")
		self.ktest("prefx step down", [e,T(""),z], 0, "down", 
			None, 2, 2)
		assert z.get_pref_col((20,)) == 2
		
		
class ColumnsTest(unittest.TestCase):
	def cwtest(self, desc, l, divide, size, exp):
		c = urwid.Columns( l, divide )
		rval = c.column_widths( size )
		assert rval == exp, "%s expected %s, got %s"%(desc,exp,rval)

	def test_widths(self):
		x = None # sample "column"
		self.cwtest( "simple 1", [x], 0, (20,), [20] )
		self.cwtest( "simple 2", [x,x], 0, (20,), [10,10] )
		self.cwtest( "simple 2+1", [x,x], 1, (20,), [10,9] )
		self.cwtest( "simple 3+1", [x,x,x], 1, (20,), [6,6,6] )
		self.cwtest( "simple 3+2", [x,x,x], 2, (20,), [5,6,5] )
		self.cwtest( "simple 3+2", [x,x,x], 2, (21,), [6,6,5] )
		self.cwtest( "simple 4+1", [x,x,x,x], 1, (25,), [6,5,6,5] )
		self.cwtest( "squish 4+1", [x,x,x,x], 1, (7,), [1,1,1,1] )
		self.cwtest( "squish 4+1", [x,x,x,x], 1, (6,), [1,2,1] )
		self.cwtest( "squish 4+1", [x,x,x,x], 1, (4,), [2,1] )
		
		self.cwtest( "fixed 3", [('fixed',4,x),('fixed',6,x),
			('fixed',2,x)], 1, (25,), [4,6,2] )
		self.cwtest( "fixed 3 cut", [('fixed',4,x),('fixed',6,x),
			('fixed',2,x)], 1, (13,), [4,6] )
		self.cwtest( "fixed 3 cut2", [('fixed',4,x),('fixed',6,x),
			('fixed',2,x)], 1, (10,), [4] )
		
		self.cwtest( "mixed 4", [('weight',2,x),('fixed',5,x),
			x, ('weight',3,x)], 1, (14,), [2,5,1,3] )
		self.cwtest( "mixed 4 a", [('weight',2,x),('fixed',5,x),
			x, ('weight',3,x)], 1, (12,), [1,5,1,2] )
		self.cwtest( "mixed 4 b", [('weight',2,x),('fixed',5,x),
			x, ('weight',3,x)], 1, (10,), [2,5,1] )
		self.cwtest( "mixed 4 c", [('weight',2,x),('fixed',5,x),
			x, ('weight',3,x)], 1, (20,), [4,5,2,6] )
	
	def mctest(self, desc, l, divide, size, col, row, exp, f_col, pref_col):
		c = urwid.Columns( l, divide )
		rval = c.move_cursor_to_coords( size, col, row )
		assert rval == exp, "%s expected %s, got %s"%(desc,`exp`,`rval`)
		assert c.focus_col == f_col, "%s expected focus_col %s got %s"%(
			desc, f_col, c.focus_col)
		pc = c.get_pref_col( size )
		assert pc == pref_col, "%s expected pref_col %s, got %s"%(
			desc, pref_col, pc)
		
	def test_move_cursor(self):	
		e, s, x = urwid.Edit("",""),SelectableText(""), urwid.Text("")
		self.mctest("nothing selectbl",[x,x,x],1,(20,),9,0,False,0,None)
		self.mctest("dead on",[x,s,x],1,(20,),9,0,True,1,9)
		self.mctest("l edge",[x,s,x],1,(20,),6,0,True,1,6)
		self.mctest("r edge",[x,s,x],1,(20,),13,0,True,1,13)
		self.mctest("l off",[x,s,x],1,(20,),2,0,True,1,2)
		self.mctest("r off",[x,s,x],1,(20,),17,0,True,1,17)
		self.mctest("l off 2",[x,x,s],1,(20,),2,0,True,2,2)
		self.mctest("r off 2",[s,x,x],1,(20,),17,0,True,0,17)
		
		self.mctest("l between",[s,s,x],1,(20,),6,0,True,0,6)
		self.mctest("r between",[x,s,s],1,(20,),13,0,True,1,13)
		self.mctest("l between 2l",[s,s,x],2,(22,),6,0,True,0,6)
		self.mctest("r between 2l",[x,s,s],2,(22,),14,0,True,1,14)
		self.mctest("l between 2r",[s,s,x],2,(22,),7,0,True,1,7)
		self.mctest("r between 2r",[x,s,s],2,(22,),15,0,True,2,15)
		
		# unfortunate pref_col shifting
		self.mctest("l e edge",[x,e,x],1,(20,),6,0,True,1,7)
		self.mctest("r e edge",[x,e,x],1,(20,),13,0,True,1,12)
		
		
		
	

def test_main():
	for t in [
		WithinDoubleByteTest,
		CalcBreaksCharTest,
		CalcBreaksDBCharTest,
		CalcBreaksWordTest,
		CalcBreaksWordTest2,
		CalcBreaksDBWordTest,
		CalcTranslateCharTest,
		CalcTranslateWordTest,
		CalcTranslateClipTest,
		CalcTranslateDBClipTest,
		CalcPosTest,
		Pos2CoordsTest,
		ShiftTransTest,
		TagMarkupTest,
		TextTest,
		EditTest,
		EditRenderTest,
		ListBoxCalculateVisibleTest,
		ListBoxChangeFocusTest,
		ListBoxRenderTest,
		ListBoxKeypressTest,
		PaddingTest,
		FillerTest,
		FrameTest,
		PileTest,
		ColumnsTest,
		]:
		if test_support.run_unittest(t): break
	

if __name__ == '__main__': test_main()

