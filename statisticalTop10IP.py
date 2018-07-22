#!/usr/bin/env python
# -*- coding: utf-8 -*-
#查出数据库中出现的地址信息,放入set
def select_country() :
	return
def select_province() :
	return
def select_city() :
	return

#从数据库中根据时间戳查的数据
def select_real_sip() :
	return
def select_weak_sip() :
	return
def select_month_sip() :
	return
def select_real_dip() :
	return
def select_weak_dip() :
	return
def select_month_dip() :
	return

#存入redis,是否设置ttl时间
def storeRedis(ttl_time, data) :
	return
def count(result) :
	sip_dict = {}
	dip_dict = {}
	sip_real_dict = {}
	dip_real_dict = {}
	sip_weak_dict = {}
	dip_weak_dict = {}
	sip_month_dict = {}
	dip_month_dict = {}

	sip_dict["real"] = sip_real_dict
	sip_dict["weak"] = sip_weak_dict
	sip_dict["month"] = sip_month_dict
	dip_dict["real"] = dip_real_dict
	dip_dict["weak"] = dip_weak_dict
	dip_dict["month"] = dip_month_dict
	#赋值
	location(result, sip_real_dict)
	print sip_dict
	################
	#location(select_weak_sip(), sip_weak_dict)
	#location(select_month_sip(), sip_month_dict)
	#location(select_real_sip(), dip_real_dict)
	#location(select_weak_sip(), dip_weak_dict)
	#location(select_month_sip(), dip_month_dict)


def location(data, dict_data) :
	country = select_country()
	province = select_province()
	city = select_city()
	# 给他们赋值
	for location in country :
		statisticalIP(data, location, dict_data)
	for location in province :
		statisticalIP(data, location, dict_data)
	for location in city :
		statisticalIP(data, location, dict_data)

def statisticalIP(data, location, dict_data) :
	SourceIP = {}

	for i in range(len(data[3])) :
		if data[3][i] == location :
			if SourceIP.get(data[0][i]) :
				SourceIP[data[0][i]] = SourceIP[data[0][i]] + 1
			else :
				SourceIP[data[0][i]] = 1

	dict_data[location] = statisticalTop10IP(SourceIP)



def statisticalTop10IP(SourceIP) :
	top10SourceIP = {}

	for key in SourceIP.keys() :
		count = SourceIP.get(key)
		#大小不满足直接添加到里面后移
		if len(top10SourceIP) < 10 :
			if len(top10SourceIP) == 0 :
				top10SourceIP.insert(0, key)
			for i in range(len(top10SourceIP)) :
				if SourceIP.get(top10SourceIP[i]) <= count :
					if key in top10SourceIP :
						continue
					top10SourceIP.insert(i, key)
				else :
					if key in top10SourceIP :
						continue
					top10SourceIP.append(key)
	#大小满足每次添加之后删除最后一个元素
        else :
            for i in range(len(top10SourceIP)) :
                if SourceIP.get(top10SourceIP[i]) < count:
                    #如果存在跳过
                    if key in top10SourceIP :
                        continue
                    top10SourceIP.insert(i, key)
                    #淘汰最后那个
                    top10SourceIP.pop()
	#根据ip将次数找出来,注意这里便利hash时是无序的但是你可以在redis使用zset存储,查出来时就是有序的
	top10_dict = {}
	for i in range(len(top10SourceIP)):
		top10_dict[top10SourceIP[i]] = SourceIP.get(top10SourceIP[i])
	return top10_dict