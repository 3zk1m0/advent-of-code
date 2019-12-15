from collections import defaultdict
import math

with open("day_14.txt") as f:
    line = f.readline().strip()
    lines = [line]
    while line:
        line = f.readline().strip()
        lines.append(line)
    lines.remove('')

def parse_reaction(reaction):
    result = reaction.split(' => ')[1]
    ingredients = reaction.split(' => ')[0]
    result = tuple(result.split(' '))
    ingredients = tuple([(x.split(' ')[0], x.split(' ')[1]) for x in ingredients.split(', ')])
    return  {result:ingredients}

def test_for_ore(ingredients):
    if len(ingredients.keys()) == 1:
        if list(ingredients.keys())[0] == 'ORE':
            return True
    return False

def find_recipe(ingredients, to_find):
    for item in ingredients.keys():
        if item[1] == to_find:
            recipe = item
    return {recipe: ingredients[recipe]}

def run_recipe(recipe, ingredients):
    tmp = list(recipe.keys())[0]
    recipe_output = int(tmp[0])
    the_ingredient = tmp[1]
    recipe_ingredients = recipe[tmp]
    total_output = math.ceil(ingredients[the_ingredient]/recipe_output)

    for items in recipe_ingredients:
        if items[1] in ingredients:
            ingredients[items[1]] += int(items[0])*total_output
        else:
            ingredients[items[1]] = int(items[0])*total_output

    ingredients[the_ingredient] -=  recipe_output*total_output
    return ingredients

def calc_fuel(fuel, recipe_list):
    ingredients = {'FUEL':fuel}
    while any(ingredients[key] > 0 and key != "ORE" for key in ingredients):
        keys = [key for key in ingredients if ingredients[key] > 0 and key != "ORE"][0]
        recipe = find_recipe(recipe_list, keys)
        ingredients = run_recipe(recipe, ingredients)
    return ingredients['ORE']

if __name__ == "__main__":

    recipe_list = {}

    for items in lines:
        recipe_list.update(parse_reaction(items))

    print('Part 1 = {}'.format(calc_fuel(1, recipe_list)))

    low = 0
    high = 2000000000
    while low < high:
        mid = (low + high) // 2
        req = calc_fuel(mid, recipe_list)
        if req > 1000000000000:
            high = mid - 1
        elif req < 1000000000000:
            low = mid

    print('Part 2 = {}'.format(low))
