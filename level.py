import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels

class Level:
    def __init__(self,current_level,surface,create_overworld,change_coins,change_health):
         #general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        #audio
        self.coin_sound = pygame.mixer.Sound('../audio/effects/coin.mp3')
        self.coin_sound.set_volume(0.02)
        self.kill_sound = pygame.mixer.Sound('../audio/effects/kill.wav')
        
        #overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        #player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout,change_health)

        #user interface
        self.change_coins = change_coins

        #dust
        self.dust_sprite = pygame.sprite.GroupSingle() #bracket is must**
        self.player_on_ground = False

        #expolosion particles
        self.explosion_sprite = pygame.sprite.Group()

        #terrain setup 
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        #grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout,'grass')

        #crate setup
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout,'crates')

        #coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coins')

        #foreground palms
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout,'fg palms')

		#background palms 
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout,'bg palms')

        #enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')

        #constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')

        #decoation
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20,level_width)
        self.clouds = Clouds(400,level_width,40)


    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    # for terrain
                    if type == 'terrain': #import terrain graphic from the file
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png') 
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    #for grass    
                    if type == 'grass': #import grass graphic from the file
                        grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    #for crate
                    if type == 'crates':
                        sprite = Crate(tile_size,x,y)
                    #for coins
                    if type == 'coins':
                        if val == '0': sprite = Coin(tile_size,x,y,'../graphics/coins/gold',5) #if val is 0 it importing gold coins
                        if val == '1': sprite = Coin(tile_size,x,y,'../graphics/coins/silver',1) # if val is 1 it import silver coin
                    #for foreground palms
                    if type == 'fg palms':
                        if val == '0': sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_small',38)#if val is 0 it importing small palm
                        if val == '1': sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_large',64)#if val is 0 it importing big palm
                    #for background trees 
                    if type == 'bg palms':
                        sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_bg',64)
                    #for enemy
                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y)
                    #for constraint
                    if type == 'constraint':
                        sprite = Tile(tile_size,x,y)
                    
                                     
                    sprite_group.add(sprite)


        return sprite_group     

    def player_setup(self,layout,change_health):
         for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '0':
                    x = col_index * tile_size
                    y = row_index * tile_size
                if val =='0':
                    sprite = Player((x,y),self.display_surface,self.create_jump_particles,change_health)
                    self.player.add(sprite)
                if val =='1':
                    hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites(): #checking every enemy sprite
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False): # CHECKING wether the enemy is colliding with any obstacles
                enemy.reverse() # if we are telling the the enemy to turn around

    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,-5)     
        jump_particle_sprite = ParticleEffect(pos,'jump')   
        self.dust_sprite.add(jump_particle_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidable_sprites:
                if sprite.rect.colliderect(player.collision_rect):
                    if player.direction.x < 0:
                        player.collision_rect.left = sprite.rect.right
                        player.on_left = True
                        self.current_x = player.rect.left #to prevent the player from jumping through the wall
                    elif player.direction.x > 0:
                        player.collision_rect.right = sprite.rect.left
                        player.on_right = True
                        self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
        
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True #if player is on ground then true
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom            
                    player.direction.y = 0
                    player.on_ceilling = True #if player is on ceiling then true

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:  #checking whether the player is falling or jumping
            player.on_ground = False #as the y > or < than its origin the player is not on ground so its false

    def scroll_x(self):
        #player speed
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
 
        if player_x < screen_width / 4 and direction_x < 0: #b/ the PLAYER should move to the left
            self.world_shift = 8
            player.speed = 0
        elif player_x >screen_width - (screen_width/ 4) and direction_x > 0: #b/ the PLAYER should move to the right 
            self.world_shift = -7
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 7

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
           self.player_on_ground = True

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites(): #makes sures that the particles create again and again
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust_particle)# to reduce the particles on double sides for logic

    def check_deth(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level,0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
            self.create_overworld(self.current_level,self.new_max_level)

    def check_coin_collision(self):
        collided_coinds = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites,True)
        if collided_coinds:
            for coin in collided_coinds:
                self.change_coins(coin.value)
                self.coin_sound.play()

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.kill_sound.play()
                    self.player.sprite.direction.y = -16
                    explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
                    self.explosion_sprite.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def run(self):
        #run the entire game / lvl

        #decoration
        self.sky.draw(self.display_surface)
        
        #sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface,self.world_shift)

        #backgroud palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)
       
        #dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        #terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        #enemy
        self.constraint_sprites.update(self.world_shift)
        self.enemy_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprite.update(self.world_shift)
        self.explosion_sprite.draw(self.display_surface)
        
        #crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)
       
        #grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)
       
        #coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        #foreground palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        #player sprites
        self.player.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()

        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_deth()
        self.check_win()

        self.check_coin_collision()
        self.check_enemy_collisions()

        #water
        self.water.draw(self.display_surface,self.world_shift)