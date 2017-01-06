#! /usr/bin/env python



from PIL import Image

import sys, cv2




class BSpots:
	
	def __init__(self):
		self._bright_pixels	= []
		self._data_tab		= []
		self._img_max		= 0
		self._bright_spots	= []
		self.spots_coords	= []
		self.gap			= 1
		self.tolerance		= 0.99
		self.min_spot_size	= 3
		self.x_crop_size	= 100
		self.color			= "HIGH"
		self._size_ratio	= 1
		
		
	def get_image_from_file(self, image):
		self.image						= Image.open(image)
		self._image_x, self._image_y	= self.image.size
		
	
	def get_image_from_PIL(self, image):
		self.image						= image
		self._image_x, self._image_y	= self.image.size

	
	def get_image_from_CAM(self, image):
		self.image = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB)).transpose(Image.FLIP_LEFT_RIGHT)
		self._image_x, self._image_y	= self.image.size
		
		
	def flush(self):	
		self._bright_pixels	= []
		self._data_tab		= []
		self._bright_spots	= []
		self.spots_coords	= []
		self._img_max		= 0
		
	
	def _color_tab(self):
		
		if self.color == "HIGH":
			self.image		= self.image.convert("L")
			self._data_tab	= list(self.image.getdata())
			return self._data_tab
			
		elif self.color == "RED":	color_1st, color_2nd, color_3rd	= 0, 1, 2			
		elif self.color == "GREEN":	color_1st, color_2nd, color_3rd	= 1, 0, 2
		elif self.color == "BLUE":	color_1st, color_2nd, color_3rd	= 2, 0, 1
		
		for p in list(self.work_im.getdata()):
			
			r2g = p[color_1st] - p[color_2nd]
			r2b = p[color_1st] - p[color_3rd]
			self._data_tab.append(((r2g + r2b) / 2) if r2b and r2g > 0 else 0)
													
		return self._data_tab
			
		
	def _img_preprocess(self):
		
		#self.work_im = self.image
				
		self._size_ratio = self._image_x / float(self.x_crop_size)
		if 	self._image_x > self.x_crop_size:
			Y = int(self._image_y / self._size_ratio)
			self.image	= self.image.transform((self.x_crop_size, Y),\
												Image.EXTENT,\
												(0,0, self._image_x,\
												self._image_y))

		self._work_image_x, self._work_image_y	= self.image.size												
		
		
	def _find_img_max(self):
		self._img_max	= list(sorted(self._data_tab))[int(len(self._data_tab) * self.tolerance)]

		
	def _find_bright_pixels(self):		
		for i, p in enumerate(self._data_tab):
			if p >= self._img_max:
				self._bright_pixels.append((i % self._work_image_x, i // self._work_image_x))
		
		
	def	_separateXY(self):
		
		tab_x = sorted(self._bright_pixels, key = lambda i: i[0])
		tab_y = sorted(self._bright_pixels, key = lambda i: i[1])

		temp_tab_x, temp_tab_y = [],[]

		tab_len = len(self._bright_pixels)
		if tab_len > 1:
			tab_x_count, tab_y_count = 0,0
			temp_tab_x.append([])
			temp_tab_y.append([])
			for i in range(tab_len):
				temp_tab_x[tab_x_count].append(tab_x[i])
				temp_tab_y[tab_y_count].append(tab_y[i])		
				if i < tab_len - 1:
					if (tab_x[i+1][0] - tab_x[i][0]) > self.gap:
						tab_x_count += 1
						temp_tab_x.append([])
					if (tab_y[i+1][1] - tab_y[i][1]) > self.gap:
						tab_y_count += 1
						temp_tab_y.append([])
				
		self._XY_separated = (temp_tab_x, temp_tab_y)
	
	
	def _mergeXY(self):
		spots_x, spots_y = self._XY_separated  		
		for x in spots_x:
			for y in spots_y:
				bright_spot = list(set(x).intersection(y))
				if len(bright_spot) > self.min_spot_size:
					self._bright_spots.append(bright_spot)
					
										
	def _calc_coords(self, spot):
		
		xs 		= [xy[0] for xy in spot]
		ys 		= [xy[1] for xy in spot]
		
		slen	= int(len(spot) * (self._size_ratio ** 2))
				
		xc, yc 	=	int((sum(xs)/float(len(xs))) * self._size_ratio),\
					int((sum(ys)/float(len(ys))) * self._size_ratio)
					 
		x0, y0 	= int(min(xs) * self._size_ratio), int(min(ys) * self._size_ratio)
		x1, y1	= int(max(xs) * self._size_ratio), int(max(ys) * self._size_ratio)
	
		r 		= int(((x1 - xc)**2 + (y1 -yc)**2) ** 0.5)
				
		return {"SIZE":slen, "X":xc, "Y":yc, "X0":x0, "Y0":y0, "X1":x1, "Y1":y1, "R":r}
		
		
	def analize_image(self):
		self._img_preprocess()
		self._color_tab()
		self._find_img_max()
		self._find_bright_pixels()
		self._separateXY()
		self._mergeXY()
		
		for b_spot in self._bright_spots:
			self.spots_coords.append(self._calc_coords(b_spot))
			
		return sorted(self.spots_coords, key = lambda x:x["SIZE"], reverse = True) 	
