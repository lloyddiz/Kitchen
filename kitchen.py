#!/usr/bin/python

from jinja2 import Environment, FileSystemLoader
import cherrypy, redis

class Kitchen(object):
   env = Environment(loader=FileSystemLoader("templates"))
   red = redis.StrictRedis(host='localhost', port=6379, db=0)

   def index(self, e=env, r=red):
      t = e.get_template("index.html")
      d = {}
      for k in r.keys():
         d[k] = r.get(k)
      return t.render(title="Kitchen manager",
                      header="Welcome to your kitchen manager",
                      ingredients=d)

   def add(self, e=env):
      t = e.get_template("add.html")
      return t.render(title="Add ingredients to kitchen", header="Welcome to your kitchen manager")

   def remove(self, ingredient, e=env, r=red):
      r.delete(ingredient)
      raise cherrypy.HTTPRedirect("/")

   def add2list(self, ingredient, unit, quantity, r=red):
      k = ingredient + " " + unit
      v = quantity
      r.set(k,v)
      raise cherrypy.HTTPRedirect("/")

   def mod(self, ingredient, e=env, r=red):
      t = e.get_template("mod.html")
      i = ingredient.split(" ")[0]
      u = ingredient.split(" ")[1] # !!! may be more than 2 elements !
      q = r.get(ingredient)
      return t.render(title="Add ingredients to kitchen",
                      header="Welcome to PTL's kitchen manager",
                      ingr=i,
                      unit=u,
                      qty=q)

   def modingredient(self, ingredient, new_ingredient, new_unit, new_quantity, r=red):
      new_ingr_name = new_ingredient + " " + new_unit
      new_qtty = new_quantity
      if ingredient != new_ingr_name:
         r.rename(ingredient, new_ingr_name)
      r.set(new_ingr_name, new_quantity)
      raise cherrypy.HTTPRedirect("/")

   index.exposed  = True
   add.exposed    = True
   remove.exposed = True
   add2list.exposed = True
   mod.exposed = True
   modingredient.exposed = True



cherrypy.quickstart(Kitchen())
