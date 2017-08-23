from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from wagtail.wagtailcore import hooks


class TestHooks(TestCase):
    fixtures = ['test.json']

    def test_menus_modify_sub_menu_items(self):

        @hooks.register('menus_modify_sub_menu_items')
        def modify_sub_menu_items(menu_items, page, request, **kwargs):
            current_level = kwargs['current_level']
            self.assertTrue('current_site' in kwargs)
            self.assertTrue('current_page' in kwargs)
            self.assertTrue('current_page_ancestor_ids' in kwargs)
            self.assertTrue('use_specific' in kwargs)
            self.assertTrue('menu_instance' in kwargs)
            self.assertTrue('check_for_children' in kwargs)
            self.assertTrue('allow_repeating_parents' in kwargs)
            self.assertTrue('apply_active_classes' in kwargs)
            self.assertTrue('use_absolute_page_urls' in kwargs)
            if current_level == 1:
                menu_items.append({
                    'href': 'https://facebook.com',
                    'text': 'Visit facebook',
                    'active_class': 'external',
                })
            return menu_items

        """
        Let's render the test homepage to see what happens
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Visit facebook', 5)
        print(response)
