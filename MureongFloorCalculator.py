##################################################
# 공식
#
# 데미지 = [ (주스탯 * 4 + 부스탯) * 총 공격력 * 무기상수 * 직업보정상수 / 100 ] 
#           * (스킬 퍼뎀 / 100) * 크리티컬 데미지 보정 * [ (100 + 공격력%) / 100 ] * 
#           [ (100 + 데미지% + 보공%) / 100 ] * 방어율 무시 보정 * 렙차 보정 * 숙련도 보정 
#           * [ (모든 최종데미지 계산값% + 100) / 100 ] 
#
# 스공 = [(주스텟*4+부스텟)/100]*(총 공/마)*[(100+데미지%)/100]*
#           [(100+최종 데미지)/100]*[(100+공/마%)/100]*무기상수*직업상수
#
#
# 데미지 = 스공 / 데미지% / 최종데미지% * (보공+데미지 %) * 크뎀보정 * 방무보정 * 스킬퍼뎀 * 레벨뻥 * 코강
#
################################################

import os
from dotenv import dotenv_values

config = dotenv_values("Character.property.ini")

################################################
# 무기상수 너클
WEAPONRATE = 1.7
# 직업상수 은월 
JOBCORRECTION = 1
################################################

################################################
# 진귀참 한줄뎀 30랩 기준
# 720% 방무 50%
SKILLDAMAGE = 7.2 
SKILLIGNORE = 50
HYPERBOSSDMG = 20
HYPERDAMGE = 20
VCOREIGNORE = 20
###############################################

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

# 제네무기 -> true 
WEAPONETYPE = str2bool(config['GenesisWeapon'])


#########
# 계산식 
#########

# 옵드, 정결극, 집속, 오쓰, 메여축, 귀문진 등 추가 버프 고려하지 않음
# 약점 간파 25% 적용하지 않음
def CriticalDamageCorrection (crtDmg):
    return 1.35 + (crtDmg / 100)

# 스탯창에 보이지 않는 코강 방무 적용
def DefenseRateCorrection (monsterDefenseRate, ignoreDef):
    defense = (1 - (1- ignoreDef/100)  * (1 - SKILLIGNORE/100) * (1 - VCOREIGNORE/100))
    return (100 - (monsterDefenseRate - (monsterDefenseRate * defense))) /100

# 랩뻥 계산
# 30층대 평균 진귀참 데미지
def LevelCorrection (mLev, cLev):
    levelInterval = cLev - mLev
    damage = 100
    if levelInterval >= 5 :
        damage = 120
    elif  0 <= levelInterval < 5 :
        damage = 120 - 2*5-levelInterval
    elif -9 <= levelInterval < 0 :
        damage = 90 + 5*levelInterval+4
    elif -11 <= levelInterval < -9  :
        damage = 100 + 2.5*levelInterval
    elif -20 <= levelInterval < -10 :
        damage = 120 - 2.5*8-levelInterval
    elif  -40 <= levelInterval < -20 :
        damage = 100 + 2.5*levelInterval
    else :
        damage = 0

    return damage/100


def AvgStatAtt (statAtt1, statAtt2):
    return (statAtt1 + statAtt2)/2
    
# 인텐시브 어썰트 데미지 상추뎀
def LinkSkill (level):
    return 6*level;

# 스탯창에 적용되지 않는 모법 링크 데미지 적용
def LinkSkill2 (level):
    return 3*round(level/2)

# 스탯창에 적용되지 않는 모법 링크 방무 적용
def LinkSkill2DEF (level):
    ignore = (1 - round(level/2))**3
    return ignore

def SkillCoreLevel (level):
    return 2*level;

def VSkillCoreLevel (level):
    return (540 + 6 * level)/100;

# 어빌 상추뎀 사용시 데미지 입력
def AbilityDamage (percent):
    return percent

  
def CalcLineDamage(statAtt1, statAtt2, damage, bossDamage, finalDamage, criticalDamageRate, monsterDefenseRate, ignoreDefenseRate, linkLevel, linkLevel2, abilPoint, skillLevel, vSkillLevel, monsterLevel, characterLevel):
    lineDamage = AvgStatAtt (statAtt1, statAtt2) / ((100 + damage)/100) / ((100 + finalDamage)/100) * ((100 + bossDamage + damage + HYPERBOSSDMG + HYPERDAMGE + LinkSkill(linkLevel) + LinkSkill2(linkLevel2) + AbilityDamage(abilPoint)) /100) * CriticalDamageCorrection(criticalDamageRate) * DefenseRateCorrection(monsterDefenseRate, ignoreDefenseRate) * VSkillCoreLevel(vSkillLevel) * ((100 + SkillCoreLevel(skillLevel)) / 100 * (100 + finalDamage) / 100) * LevelCorrection(monsterLevel, characterLevel)

    return lineDamage

  
def CalcMureong(lineDamage, isGenesis: bool):
    lineDamage = lineDamage / 100000000
    floor = 49
    if 1.5 < lineDamage :
        floor = 50
    elif 1.8 < lineDamage :
        floor = 51
    elif 2.5 < lineDamage :
        floor = 52
    elif 3.0 < lineDamage :
        floor = 53
    elif 3.5 < lineDamage :
        floor = 54
    elif 4.0 < lineDamage :
        floor = 55
    elif 4.8 < lineDamage :
        floor = 56
    elif 5.5 < lineDamage :
        floor = 57
    elif 6.2 < lineDamage :
        floor = 58
    elif 7.0 < lineDamage :
        floor = 59
    elif 8.3 < lineDamage or (7.8 < lineDamage and isGenesis):
        floor = 60
    elif 9.0 < lineDamage or (8.6 < lineDamage and isGenesis):
        floor = 61
    elif 10.5 < lineDamage or (10.0 < lineDamage and isGenesis):
        floor = 62
    elif 11.8 < lineDamage or (11.0 < lineDamage and isGenesis):
        floor = 63
    elif 13.0 < lineDamage or (12.2 < lineDamage and isGenesis):
        floor = 64
    elif 14.0 < lineDamage or (13.0 < lineDamage and isGenesis):
        floor = 65
    elif 14.8 < lineDamage and isGenesis:
        floor = 66
    elif 15.8 < lineDamage and isGenesis:
        floor = 67
    elif 16.5 < lineDamage and isGenesis:
        floor = 68
    elif 18.0 < lineDamage and isGenesis:
        floor = 69
    elif 21.0 < lineDamage and isGenesis:
        floor = 70

    return str(floor) + '이하'


  

stat2 = float(config['stat2'])
stat1 = float(config['stat1'])
damage = float(config['damage'])
bossDamage = float(config['bossDamage'])
finalDamage = float(config['finalDamage'])
ignoreDefenseRate = float(config['ignoreDefenseRate'])
criticalDamage = float(config['criticalDamage'])
monsterLevel = float(config['monsterLevel'])
characterLevel = float(config['characterLevel'])
monsterDefenseRate = float(config['monsterDefenseRate'])
linkLevel = float(config['linkLevel'])
linkLevel2 = float(config['linkLevel2'])
abilityPoint = float(config['abilityPoint'])
skillLevel = float(config['skillLevel'])
vSkillLevel = float(config['vSkillLevel'])


lineDamage = CalcLineDamage(stat1, stat2, damage, bossDamage, finalDamage, criticalDamage, monsterDefenseRate, ignoreDefenseRate, linkLevel, linkLevel2, abilityPoint, skillLevel, vSkillLevel, monsterLevel, characterLevel)

mureongFloor = CalcMureong(lineDamage, WEAPONETYPE)

print('보다 정확한 층수 계산을 위해 50층 이상의 데이터만 유효합니다.')

print(f'진귀참 한줄 데미지 : {lineDamage:.0f}')
print(f'예상 무릉 층수 : {mureongFloor}')

print('Thanks to 이샛기, 엘크라우치, 하요하이룽, 볼드모트 무릉연구소')

input()
