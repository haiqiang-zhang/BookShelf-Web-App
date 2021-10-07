from flask import Blueprint, render_template, url_for, request, redirect

from library.adapters.repository import AbstractRepository
from library.domain.model import *



def get_tag_choice(repo_instance:AbstractRepository,user:User):
    all_tag = repo_instance.get_tags()
    user_tag = user.tags
    return [tag.tag_name for tag in all_tag if tag not in user_tag]


def get_tags(user:User):
    user_tag = user.tags
    return user_tag

def add_tag(user:User, tag:Tag, repo_instance:AbstractRepository):
    user.tags.append(tag)
    repo_instance.commit()



