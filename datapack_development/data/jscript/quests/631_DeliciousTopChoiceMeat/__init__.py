# Made by Renji v0.1
import sys
from net.sf.l2j import Config
from net.sf.l2j.gameserver.model.quest import State
from net.sf.l2j.gameserver.model.quest import QuestState
from net.sf.l2j.gameserver.model.quest.jython import QuestJython as JQuest

qn = "631_DeliciousTopChoiceMeat"

#NPC
TUNATUN = 31537

#ITEMS
TOP_QUALITY_MEAT = 7546

#REWARDS
MOLD_GLUE,MOLD_LUBRICANT,MOLD_HARDENER,ENRIA,ASOFE,THONS = 4039,4040,4041,4042,4043,4044
REWARDS={"1":[MOLD_GLUE,15],"2":[ASOFE,15],"3":[THONS,15],"4":[MOLD_LUBRICANT,10],"5":[ENRIA,10],"6":[MOLD_HARDENER,5]}


class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onEvent (self,event,st) :
   htmltext = event
   if event == "31537-03.htm" :
     st.set("cond","1")
     st.setState(STARTED)
     st.playSound("ItemSound.quest_accept")
   elif event == "31537-05.htm" and st.getQuestItemsCount(TOP_QUALITY_MEAT) == 120 :
     st.set("cond","3")
   elif event in REWARDS.keys() :
     htmltext = "31537-07.htm"
     item,qty=REWARDS[event]
     if st.getQuestItemsCount(TOP_QUALITY_MEAT) == 120 and st.getInt("cond") == 3:
       htmltext = "31537-06.htm"
       st.takeItems(TOP_QUALITY_MEAT,120)
       st.giveItems(item,int(qty*Config.RATE_QUESTS_REWARD))
       st.playSound("ItemSound.quest_finish")
       st.exitQuest(1)
   return htmltext

 def onTalk (self,npc,player):
   st = player.getQuestState(qn)
   if st :
        npcId = npc.getNpcId()
        htmltext = "<html><head><body>I have nothing to say you</body></html>"
        id = st.getState()
        cond = st.getInt("cond")
        if cond == 0 :
            if player.getLevel() >= 65 :
                htmltext = "31537-01.htm"
            else:
                htmltext = "31537-02.htm"
                st.exitQuest(1)
        elif id == STARTED :
            if cond == 1 :
                htmltext = "31537-01a.htm"
            elif cond == 2 and st.getQuestItemsCount(TOP_QUALITY_MEAT) == 120 :
                htmltext = "31537-04.htm"
            elif cond == 3 :
                htmltext = "31537-05.htm"
   return htmltext

 def onKill (self,npc,player):
   partyMember = self.getRandomPartyMember(player, "1")
   if not partyMember: return
   st = partyMember.getQuestState(qn)
   if st :
        if st.getState() == STARTED :
            count = st.getQuestItemsCount(TOP_QUALITY_MEAT)
            if st.getInt("cond") == 1 and count < 120 :
              st.giveItems(TOP_QUALITY_MEAT,1)
              if count == 119 :
                st.playSound("ItemSound.quest_middle")
                st.set("cond","2")
              else:
                st.playSound("ItemSound.quest_itemget")  
   return

QUEST       = Quest(631,qn,"Delicious Top Choice Meat")
CREATED     = State('Start', QUEST)
STARTED     = State('Started', QUEST)

QUEST.setInitialState(CREATED)
QUEST.addStartNpc(TUNATUN)

QUEST.addTalkId(TUNATUN)

QUEST.addKillId(21451)
QUEST.addKillId(21470)
QUEST.addKillId(21489)

STARTED.addQuestDrop(21451,TOP_QUALITY_MEAT,1)

print "importing quests: 631: Delicious Top Choice Meat"
