#coding:utf-8
import urllib2
import json

def xiaohuangji(ask):
	ask = ask.encode('UTF-8')

	enask = urllib2.quote(ask)
	send_headers = {
			'Cookie': 'SimSimiSid=s%3AC-Iqb1i97eFfUTnI0NVrb0ALRxqmFOhI.cgwVyYOildkw7SLbpiJR9ZbTv46vN7odWSm6pUHmUt8; AWSELB=B9551BF112497261E578B202D2B846B8A14A9E164925C9E49AE38073AD731E9339F9CF3D5103EBDD4C47F84244016C7397B26926368A8594CAC5AB79099CD419DF99533536; uid=53960076; _ga=GA1.2.796850059.1436366601; _gat=1'
#    'Cookie':'Filtering=0.0; Filtering=0.0; isFirst=1; isFirst=1; simsimi_uid=50840753; simsimi_uid=50840753; teach_btn_url=talk; teach_btn_url=talk; sid=s%3AzwUdofEDCGbrhxyE0sxhKEkF.1wDJhD%2BASBfDiZdvI%2F16VvgTJO7xJb3ZZYT8yLIHVxw; selected_nc=zh; selected_nc=zh; menuType=web; menuType=web; __utma=119922954.2139724797.1396516513.1396516513.1396703679.3; __utmc=119922954; __utmz=119922954.1396516513.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
  }
	baseurl = r'http://www.simsimi.com/requestChat?lc=zh&ft=1.0&req='
	url = baseurl+enask+'&uid=53960076'
	req = urllib2.Request(url,headers=send_headers)
	resp = urllib2.urlopen(req)
	reson = json.loads(resp.read())
	rt = reson['res']
	if u'崔祎彤' in rt :
		rt=rt.replace(u'崔祎彤',u'张晓梅')
	if u'党泽梁' in rt :
		rt=rt.replace(u'党泽梁',u'胡国君')
	if u'小黄鸡' in rt :
		rt=rt.replace(u'小黄鸡',u'小潼潼')
	if u'鸡' in rt :
		rt=rt.replace(u'鸡',u'人')
	if u'simsim' in rt:
		rt=rt.replace(u'simsim',u'潼潼')

	return rt
