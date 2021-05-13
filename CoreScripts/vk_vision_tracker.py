from valkyrie import *
from helpers.drawings import Circle
from time import time
import json

show_clones, show_wards, show_traps = None, None, None
circle_mm	= Circle(0.0, 15, 1.0, Col.Red, False, True, mode = 0)
circle_world = Circle(0.0, 50, 3.0, Col.Red, False, True)

size_clone = 40
size_wards = 40
size_traps = 40

traps = {
	#Name -> (radius, show_radius_circle, show_radius_circle_minimap, icon)					  
	'caitlyntrap'		  : [50,  True,  False, "caitlyn_yordlesnaptrap"],
	'jhintrap'			 : [140, True,  False, "jhin_e"],
	'jinxmine'			 : [50,  True,  False, "jinx_e"],
	'maokaisproutling'	 : [50,  False, False, "maokai_e"],
	'nidaleespear'		 : [50,  True,  False, "nidalee_w1"],
	'shacobox'			 : [300, True,  False, "jester_deathward"],
	'teemomushroom'		: [75,  True,  True,  "teemo_r"]
}

wards = {
	'jammerdevice'		 : [900, True, True, "pinkward"],
	'perkszombieward'	  : [900, True, True, "bluetrinket"],
	'bluetrinket'		  : [900, True, True, "bluetrinket"],
	'yellowtrinket'		: [900, True, True, "yellowtrinket"],
	'yellowtrinketupgrade' : [900, True, True, "yellowtrinket"],
	'sightward'			: [900, True, True, "sightward"],
	'visionward'		   : [900, True, True, "sightward"],
	'ward'				 : [900, True, True, "sightward"],
}

clones = {
	'shaco'				: [0, False, False, "jester_hallucinogenbomb"],
	'leblanc'			  : [0, False, False, "leblancmirrorimage"],
	'monkeyking'		   : [0, False, False, "monkeykingdecoy"],
	'neeko'				: [0, False, False, "neeko_w"],
	'fiddlestickseffigy'   : [0, False, False, "fiddlesticksp2.fiddlesticksrework"],
}

def draw_settings(ui, objs, label):
	ui.text(label + ' Settings', Col.Purple)
	for x in objs.keys():
		ui.image(objs[x][-1], Vec2(15, 15))
		ui.sameline()
		if ui.beginmenu(x):
			objs[x][1] = ui.checkbox("Show range circles", objs[x][1])
			objs[x][2] = ui.checkbox("Show range circles on minimap", objs[x][2])
			
			ui.endmenu()

def valkyrie_menu(ctx: Context):
	global show_clones, show_wards, show_traps, traps, wards
	global size_clone, size_traps, size_wards
	global circle_mm, circle_world
	ui = ctx.ui
	
	ui.text('Global Settings', Col.Purple)
	circle_world.ui("Circle world settings", ctx)
	circle_mm.ui("Circle minimap settings", ctx)
	size_clone = ui.sliderint('Size icon clones', size_clone, 10, 100)
	size_traps = ui.sliderint('Size icon traps', size_traps, 10, 100)
	size_wards = ui.sliderint('Size icon wards', size_wards, 10, 100)
	
	ui.image('jester_hallucinogenbomb', Vec2(size_clone, size_clone))
	ui.sameline()
	ui.image('caitlyn_yordlesnaptrap', Vec2(size_traps, size_traps))
	ui.sameline()
	ui.image('pinkward', Vec2(size_wards, size_wards))
	
	show_clones = ui.checkbox("Show clones", show_clones)
	show_wards  = ui.checkbox("Show wards", show_wards)
	show_traps  = ui.checkbox("Show traps", show_traps)
	ui.separator()

	draw_settings(ui, traps, "Traps")
	draw_settings(ui, wards, "Wards")

def valkyrie_on_load(ctx: Context):
	global show_clones, show_wards, show_traps, traps, wards
	global size_clone, size_traps, size_wards
	global circle_mm, circle_world
	cfg = ctx.cfg

	show_clones = cfg.get_bool("show_clones", True)
	show_wards = cfg.get_bool("show_wards", True)
	show_traps = cfg.get_bool("show_traps", True)
	
	size_clone = cfg.get_int("size_clone", size_clone)
	size_wards = cfg.get_int("size_wards", size_wards)
	size_traps = cfg.get_int("size_traps", size_traps)
	
	traps = json.loads(cfg.get_str("traps", json.dumps(traps)))
	wards = json.loads(cfg.get_str("wards", json.dumps(wards)))
	
	circle_world = Circle.from_str(cfg.get_str("circle_world", str(circle_world)))
	circle_mm	= Circle.from_str(cfg.get_str("circle_mm",	str(circle_mm)))
	
def valkyrie_on_save(ctx: Context):
	cfg = ctx.cfg
	
	cfg.set_bool("show_clones", show_clones)
	cfg.set_bool("show_wards", show_wards)
	cfg.set_bool("show_traps", show_traps)
	
	cfg.set_str("circle_world", str(circle_world))
	cfg.set_str("circle_mm", str(circle_mm))
	
	cfg.set_str("traps", json.dumps(traps))
	cfg.set_str("wards", json.dumps(wards))
	
	cfg.set_int('size_traps', size_traps)
	cfg.set_int('size_clone', size_clone)
	cfg.set_int('size_wards', size_wards)
	
def draw(ctx, obj, size, radius, show_circle_world, show_circle_map, icon):
	
	pos = ctx.w2s(obj.pos)

	if ctx.is_on_screen(pos):
		duration = obj.expiry + obj.last_seen - ctx.time
		offset = (time()*100 % 200.0)
		offset = 100.0 - (offset - 100.0) if offset > 100.0 else offset
		ctx.image(icon, Vec3(obj.pos.x, obj.pos.y + offset, obj.pos.z), Vec2(size, size), Col(1.0, 1.0, 1.0, 0.8))
		#ctx.image(icon, pos, Vec2(size, size), Col.White, 10)
		
		if duration > 0.0:
			pos.y += size/2 + 8
			ctx.text(pos, str(int(duration)), Col.White)
		if show_circle_world:
			circle_world.radius = radius
			circle_world.draw_at(ctx, obj.pos)
	
	if show_circle_map:
		circle_mm.radius = ctx.d2m(radius)
		circle_mm.draw_at(ctx, ctx.w2m(obj.pos))

def valkyrie_exec(ctx: Context):

	for obj in ctx.others.alive().enemy_to(ctx.player).get():
		if show_wards and obj.has_tags(Unit.Ward) and obj.name in wards:
			draw(ctx, obj, size_wards, *(wards[obj.name]))
		elif show_traps and obj.has_tags(Unit.SpecialTrap) and obj.name in traps:
			draw(ctx, obj, size_traps, *(traps[obj.name]))
	
	if show_clones:
		for champ in ctx.champs.clone().alive().enemy_to(ctx.player).get():
			if champ.name in clones:
				draw(ctx, champ, size_clone, *(clones[champ.name]))