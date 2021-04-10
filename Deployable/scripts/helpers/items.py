from valkyrie import *

def crit_from_items(item_slots):
	crit = 0.0
	for slot in item_slots:
		if slot.item:
			crit += slot.item.crit
	return crit

def onhit_guinsoo(src, target):
	return min(200.0, min(crit_from_items(src.item_slots), 1.0) * 100.0 * 2.0)
	
def onhit_rageknife(src, target):
	return min(175.0, min(crit_from_items(src.item_slots), 1.0) * 100.0 * 1.75)

def onhit_noonquiver(src, target):
	return 0.0 if target.has_tags(Unit.Champion) else 20.0
	
def onhit_recurve_bow(src, target):
	return 15.0
	
def onhit_botrk(src, target):
	dmg = target.health * (0.06 if src.is_ranged else 0.1)
	if dmg > 60.0 and not target.has_tags(Unit.Champion):
		return 60.0
	return dmg
	
def onhit_doran_ring(src, target):
	return 5.0
	
def onhit_nashors(src, target):
	return 15.0 + 0.2 * src.ap
	
def onhit_wits_end(src, target):
	return 15.0 + 3.82 * (src.lvl - 1)

OnHit_Physical = {
	3124: onhit_guinsoo,
	6677: onhit_rageknife,	
	6670: onhit_noonquiver,
	1043: onhit_recurve_bow,
	3153: onhit_botrk,
	1056: onhit_doran_ring
}

OnHit_Magical = {
	3115: onhit_nashors,
	3091: onhit_wits_end
}

def get_onhit_physical(source, target):
	global OnHit_Physical
	
	phys = source.base_atk + source.bonus_atk
	for slot in source.item_slots:
		item = slot.item
		if item and item.id in OnHit_Physical:
			phys += OnHit_Physical[item.id](source, target)
			
	return (phys*100.0)/(100.0 + target.armor)
	
def get_onhit_magical(source, target):
	global OnHit_Magical
	
	magical = 0.0
	for slot in source.item_slots:
		item = slot.item
		if item and item.id in OnHit_Magical:
			magical += OnHit_Magical[item.id](source, target)
			
	return (magical*100.0)/(100.0 + target.magic_res)