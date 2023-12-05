from datetime import datetime, timedelta
from loader import admin_link

def get_plural(count, words):
	words_list = words.split(', ')
	last_digit = int(str(count)[-1])
	if last_digit == 1 and count != 11:
		return words_list[0]
	if last_digit in [2, 3, 4] and count not in [12, 13, 14]:
		return words_list[1]
	return words_list[2]

class TimeDifference():
	def __init__(self, start, end):
		"""
		By @IsHeCoder.
		"""
		self.years = 0
		self.months = 0
		self.weaks = 0
		self.days = 0
		self.hours = 0
		self.minutes = 0
		self.seconds = 0

		self.difference = end - start
		
		if self.difference >= timedelta(seconds=1):
			self.seconds = self.difference.seconds % 3600 % 60
			if self.difference >= timedelta(minutes=1):
				self.minutes = int(self.difference.total_seconds()//60 % 60)
				if self.difference >= timedelta(hours=1):
					self.hours = int(self.difference.total_seconds()//3600 % 24)
					if self.difference >= timedelta(days=1):
						self.days = self.difference.days % 30
						if self.difference >= timedelta(days=7):
							self.weaks = self.days // 7
							self.days = self.days % 7
							if self.difference >= timedelta(days=30):	
								self.months = int(self.difference.days //30 % 12)
								if self.difference >= timedelta(days=365):
									self.years = int(self.difference.days // 365)
	def get_difference(self, withHTML: bool = False) -> str:
		"""
		By @IsHeCoder. Use withHTML if you need to to get a bold difference.	
		:param withHTML:	
		:return:
		"""
		out = ''
		if withHTML:
			if self.years:
				out += f'<b>{self.years}</b> {get_plural(self.years, "год, года, лет")}, '
			if self.months:
				out += f'<b>{self.months}</b> {get_plural(self.months, "месяц, месяца, месяцев")}, '
			if self.weaks:
				out += f'<b>{self.weaks}</b> {get_plural(self.weaks, "неделю, недели, недель")}, '
			if self.days:
				out += f'<b>{self.days}</b> {get_plural(self.days, "день, дня, дней")}, '
			if self.hours:
				out += f'<b>{self.hours}</b> {get_plural(self.hours, "час, часа, часов")} и '
			if self.minutes:
				out += f'<b>{self.minutes}</b> {get_plural(self.minutes, "минуту, минуты, минут")}.'
			else:
				out += f'<b>{self.seconds}</b> {get_plural(self.seconds, "секунду, секунды, секунд")}.'
		else:
			if self.years:
				out += f'{self.years} {get_plural(self.years, "год, года, лет")}, '
			if self.months:
				out += f'{self.months} {get_plural(self.months, "месяц, месяца, месяцев")}, '
			if self.weaks:
				out += f'{self.weaks} {get_plural(self.weaks, "неделю, недели, недель")}, '
			if self.days:
				out += f'{self.days} {get_plural(self.days, "день, дня, дней")}, '
			if self.hours:
				out += f'{self.hours} {get_plural(self.hours, "час, часа, часов")} и '
			if self.minutes:
				out += f'{self.minutes} {get_plural(self.minutes, "минуту, минуты, минут")}.'
			else:
				out += f'{self.seconds} {get_plural(self.seconds, "секунду, секунды, секунд")}.'
		return out

def get_admin_link(text: str) -> str:
	return f'<a href="t.me/{admin_link}">{text}</a>'