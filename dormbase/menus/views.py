# Dormbase -- open-source dormitory database system
# Copyright (C) 2012 Alex Chernyakhovsky <achernya@mit.edu>
#                    Drew Dennison       <dennison@mit.edu>
#                    Isaac Evans         <ine@mit.edu>
#                    Luke O'Malley       <omalley1@mit.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import feedparser

def menus(request):
    # should get cached and refreshed with a cron job
    menus = feedparser.parse('http://www.cafebonappetit.com/rss/menu/402').entries

    items = []
    for i in menus:
        day = i.title_detail.value
        
        # Im sure there is a better way to do this, but feedparser is
        # giving a string to work with
        dishes = i.summary_detail.value
        dishes = dishes.replace('</h4>', '')
        dishes = dishes.replace('\n', '')
        dishes = dishes.replace('<p>', '')
        dishes = dishes.replace('</p>', '')
        dishes = dishes.replace(';', ': ')
        dishes = dishes.replace('&nbsp', '')

        # The first element is ignored becase it is empty
        dishes = dishes.split('<h4>')[1:]

        items.append({'day': day, 'dishes': dishes})

    payload = {'menus': items}
    print payload

    return render_to_response('menus/menus.html', payload, context_instance = RequestContext(request))