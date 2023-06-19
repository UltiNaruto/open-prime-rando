import dataclasses

from retro_data_structures.enums import echoes
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.WeaponVulnerability import WeaponVulnerability
from retro_data_structures.properties.echoes.core.Color import Color
from retro_data_structures.properties.echoes.core.Vector import Vector
from retro_data_structures.crc import crc32

from open_prime_rando.echoes.dock_lock_rando.dock_type import *
from open_prime_rando.echoes.dock_lock_rando.map_icons import DoorMapIcon

reflect = WeaponVulnerability(damage_multiplier=0, effect=echoes.Effect.Reflect)
vulnerable = WeaponVulnerability(damage_multiplier=100, effect=echoes.Effect.Normal)
immune = WeaponVulnerability(damage_multiplier=0, effect=echoes.Effect.Normal, ignore_radius=True)

resist_all_vuln = DamageVulnerability(
    power=reflect, dark=reflect, light=reflect, annihilator=reflect,
    power_charge=reflect, entangler=reflect, light_blast=reflect, sonic_boom=reflect,
    super_missle=reflect, black_hole=reflect, sunburst=reflect, imploder=reflect,

    boost_ball=immune, cannon_ball=immune, screw_attack=immune, bomb=immune, power_bomb=immune,
    missile=immune, phazon=reflect, ai=immune, poison_water=immune, dark_water=immune, lava=immune,
    area_damage_hot=immune, area_damage_cold=immune, area_damage_dark=immune, area_damage_light=immune,
    weapon_vulnerability=immune, normal_safe_zone=immune,
)

normal_door_model = 0x6B78FD92
dark_door_model = 0xbbcf134d
annihilator_door_model = 0xa50c7238

blast_collision_box = Vector(0.35, 5.0, 4.0)
blast_collision_offset = Vector(-2/3, 0, 2.0)

DOCK_TYPES: dict[str, DoorType] = {
    "Normal": NormalDoorType(
        name="Normal",
        vulnerability=dataclasses.replace(
            resist_all_vuln,
            power=vulnerable, dark=vulnerable, light=vulnerable, annihilator=vulnerable,
            power_charge=vulnerable, entangler=vulnerable, light_blast=vulnerable, sonic_boom=vulnerable,
            super_missle=vulnerable, black_hole=vulnerable, sunburst=vulnerable, imploder=vulnerable,

            missile=vulnerable, bomb=vulnerable, power_bomb=vulnerable,

        ),
        shell_color=Color(r=0, g=1, b=1, a=1),
        map_icon=DoorMapIcon.Normal,
    ),
    "Dark": NormalDoorType(
        name="Dark",
        vulnerability=dataclasses.replace(resist_all_vuln, dark=vulnerable, entangler=vulnerable, black_hole=vulnerable),
        shell_model=dark_door_model,
        shell_color=Color(r=1, g=1, b=1, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to most weapons. Dark energy may damage it."
        ),
        map_icon=DoorMapIcon.Dark
    ),
    "Light": NormalDoorType(
        name="Light",
        vulnerability=dataclasses.replace(resist_all_vuln, light=vulnerable, light_blast=vulnerable, sunburst=vulnerable),
        shell_color=Color(r=1, g=1, b=1, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to most weapons. Light energy may damage it."
        ),
        map_icon=DoorMapIcon.Light
    ),
    "Annihilator": NormalDoorType(
        name="Annihilator",
        vulnerability=dataclasses.replace(resist_all_vuln, annihilator=vulnerable, sonic_boom=vulnerable, imploder=vulnerable),
        shell_model=annihilator_door_model,
        shell_color=Color(r=1, g=1, b=1, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to most weapons. A mix of light and dark energy may damage it."
        ),
        map_icon=DoorMapIcon.Annihilator
    ),
    "Disabled": NormalDoorType(
        name="Disabled",
        vulnerability=resist_all_vuln,
        shell_color=Color(r=0, g=0, b=0, a=0),
        scan_text=(
            "Door system access denied.",
            "Unable to bypass security codes. Seek an alternate exit."
        ),
        map_icon=DoorMapIcon.Disabled
    ),
    "Missile": VanillaBlastShieldDoorType(
        name="Missile",
        vulnerability=dataclasses.replace(resist_all_vuln, missile=vulnerable),
        shell_color=Color(r=1, g=0, b=0, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to most weapons. A Missile blast may damage it."
        ),
        map_icon=DoorMapIcon.Missile,
        shield_model=0xBFB4A8EE,
    ),
    "SuperMissile": VanillaBlastShieldDoorType(
        name="SuperMissile",
        vulnerability=dataclasses.replace(resist_all_vuln, super_missle=vulnerable),
        shell_color=Color(r=0, g=1, b=0, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to most weapons. A Super Missile blast may damage it."
        ),
        map_icon=DoorMapIcon.SuperMissile,
        shield_model=0xF115F575,
    ),
    "PowerBomb": VanillaBlastShieldDoorType(
        name="PowerBomb",
        vulnerability=dataclasses.replace(resist_all_vuln, power_bomb=vulnerable),
        shell_color=Color(r=1, g=0.94, b=0, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to most weapons. A Power Bomb may damage it."
        ),
        map_icon=DoorMapIcon.PowerBomb,
        shield_model=0xC2E4F075,
    ),
    "SeekerMissile": SeekerBlastShieldDoorType(
        name="SeekerMissile",
        vulnerability=dataclasses.replace(resist_all_vuln, missile=vulnerable),
        shell_color=Color(r=0.5, g=0, b=0.64, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to most weapons. Five simultaneous blasts from Seeker Missiles may damage it."
        ),
        map_icon=DoorMapIcon.SeekerMissile,
        shield_model=0x56F4208B,
    ),
    "ScrewAttack": BlastShieldDoorType(
        name="ScrewAttack",
        vulnerability=dataclasses.replace(resist_all_vuln, screw_attack=vulnerable),
        shell_model=annihilator_door_model,
        shell_color=Color(r=0, g=0, b=1, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to most weapons. The Screw Attack may damage it."
        ),
        map_icon=DoorMapIcon.ScrewAttack,
        shield_model=0x56F4208B,
    ),
    "Bomb": BlastShieldDoorType(
        name="Bomb",
        vulnerability=dataclasses.replace(resist_all_vuln, bomb=vulnerable),
        shell_model=annihilator_door_model,
        shell_color=Color(r=0, g=1, b=1, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to most weapons. A Morph Ball Bomb blast may damage it."
        ),
        map_icon=DoorMapIcon.Bomb,
        shield_model=0x56F4208B,
    ),
    "Boost": BlastShieldDoorType(
        name="Boost",
        vulnerability=dataclasses.replace(resist_all_vuln, boost_ball=vulnerable, cannon_ball=vulnerable),
        shell_model=annihilator_door_model,
        shell_color=Color(r=1, g=1, b=0, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to most weapons. The Boost Ball may damage it."
        ),
        map_icon=DoorMapIcon.Boost,
        shield_model=0x56F4208B,
    ),
    "Grapple": GrappleDoorType(
        name="Grapple",
        vulnerability=resist_all_vuln,
        shell_model=annihilator_door_model,
        shell_color=Color(r=1, g=0, b=0, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to weapon fire, but is weakly secured. The Grapple Beam may be able to remove it."
        ),
        map_icon=DoorMapIcon.Grapple,
        shield_model=0x56F4208B,
    ),
    "Darkburst": BlastShieldDoorType(
        name="Darkburst",
        vulnerability=dataclasses.replace(resist_all_vuln, black_hole=vulnerable),
        shell_model=dark_door_model,
        shell_color=Color(r=1, g=1, b=1, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to most weapons. A massive burst of dark energy may damage it."
        ),
        map_icon=DoorMapIcon.Dark,
        shield_model="custom_door_lock_darkburst.CMDL",
    ),
    "Sunburst": BlastShieldDoorType(
        name="Sunburst",
        vulnerability=dataclasses.replace(resist_all_vuln, sunburst=vulnerable),
        shell_model=normal_door_model,
        shell_color=Color(r=1, g=1, b=1, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to most weapons. A massive burst of light energy may damage it."
        ),
        map_icon=DoorMapIcon.Light,
        shield_model="custom_door_lock_sunburst.CMDL",
    ),
    "SonicBoom": BlastShieldDoorType(
        name="SonicBoom",
        vulnerability=dataclasses.replace(resist_all_vuln, imploder=vulnerable),
        shell_model=annihilator_door_model,
        shell_color=Color(r=1, g=1, b=1, a=1),
        scan_text=(
            "There is a Blast Shield on the door blocking access. ",
            "Analysis indicates that the Blast Shield is invulnerable to most weapons. A massive burst of light and dark energy may damage it."
        ),
        map_icon=DoorMapIcon.Annihilator,
        shield_model="custom_door_lock_sonicboom.CMDL",
    ),
    "AgonEnergy": PlanetaryEnergyDoorType(
        name="AgonEnergy",
        vulnerability=resist_all_vuln,
        shell_color=Color(r=0.64, g=0.34, b=0, a=1),
        scan_text=(
            "There is a Luminoth barrier on the door blocking access. ",
            "Analysis indicates that the barrier is linked to the energy of Agon. Return the energy to the Agon Temple."
        ),
        map_icon=DoorMapIcon.AgonEnergy,
        planetary_energy_item_id=-1 # TODO
    ),
    "TorvusEnergy": PlanetaryEnergyDoorType(
        name="TorvusEnergy",
        vulnerability=resist_all_vuln,
        shell_color=Color(r=0.31, g=0.59, b=38, a=1),
        scan_text=(
            "There is a Luminoth barrier on the door blocking access. ",
            "Analysis indicates that the barrier is linked to the energy of Torvus. Return the energy to the Torvus Temple."
        ),
        map_icon=DoorMapIcon.TorvusEnergy,
        planetary_energy_item_id=-1 # TODO
    ),
    "SanctuaryEnergy": PlanetaryEnergyDoorType(
        name="SanctuaryEnergy",
        vulnerability=resist_all_vuln,
        shell_color=Color(r=0.64, g=0.34, b=0, a=1),
        scan_text=(
            "There is a Luminoth barrier on the door blocking access. ",
            "Analysis indicates that the barrier is linked to the energy of Sanctuary. Return the energy to the Sanctuary Temple."
        ),
        map_icon=DoorMapIcon.AgonEnergy,
        planetary_energy_item_id=-1 # TODO
    ),
}
