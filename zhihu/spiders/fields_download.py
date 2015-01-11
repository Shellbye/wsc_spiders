__author__ = 'shellbye'


class FieldsDownload(object):
    user_reputation_fields = {
        'vote_count': {
            'method': 'xpath',
            'params': "//i[@class='zm-profile-icon zm-profile-icon-vote']/following-sibling::span/strong/text()",
        },
        'thank_count': {
            'method': 'xpath',
            'params': "//i[@class='zm-profile-icon zm-profile-icon-thank']/following-sibling::span/strong/text()",
        },
        'fav_count': {
            'method': 'xpath',
            'params': "//i[@class='zm-profile-icon zm-profile-icon-fav']/following-sibling::span/strong/text()",
        },
        'share_count': {
            'method': 'xpath',
            'params': "//i[@class='zm-profile-icon zm-profile-icon-share']/following-sibling::span/strong/text()",
        },
    }
    user_profile_list_fields = {
        'zm-profile-icon zm-profile-icon-location': 'locations',
        'zm-profile-icon zm-profile-icon-company': 'employments',
        'zm-profile-icon zm-profile-icon-edu': 'educations',
    }
    user_answer_fields = {
        'answer_id': {
            'method': 'xpath',
            'params': "descendant::h2/a/@href",
        },
        'answer_title': {
            'method': 'xpath',
            'params': "descendant::h2/a/text()",
        },
        'answer_bio': {
            'method': 'xpath',
            'params': "descendant::h3[@class='zm-item-answer-author-wrap']/strong/@title",
        },
        'answer_vote_up': {
            'method': 'xpath',
            'params': "descendant::a[@class='zm-item-vote-count']/text()",
        },
        'answer_time': {
            'method': 'xpath',
            'params': "descendant::a[@class='answer-date-link meta-item' or "
                      "@class='answer-date-link last_updated meta-item']/text()",
        },
    }
    user_question_fields = {
        'question_id': {
            'method': 'xpath',
            'params': "descendant::a[@class='question_link']/@href",
        },
        'question_title': {
            'method': 'xpath',
            'params': "descendant::a[@class='question_link']/text()",
        },
        'question_answer_count': {
            'method': 'xpath',
            'params': "descendant::div[@class='meta zg-gray']/span[1]/following-sibling::text()",
        },
        'question_follower_count': {
            'method': 'xpath',
            'params': "descendant::div[@class='meta zg-gray']/span[2]/following-sibling::text()",
        },
        'question_view_count': {
            'method': 'xpath',
            'params': "descendant::div[@class='zm-profile-vote-num']/text()",
        },
    }
    user_profile_fields = {
        'user_data_id': {
            'method': 'xpath',
            'params': "//div[@class='zm-profile-header-op-btns clearfix']/button/@data-id",
            'default': "1166f0aae6dfccf3d89ad6e065804593",  # the crawl user's id
        },
        'user__xsrf_value': {
            'method': 'xpath',
            'params': "//input[@name='_xsrf']/@value",
            'default': "",
        },
        'name': {
            'method': 'xpath',
            'params': "//div[@class='title-section ellipsis']/span[@class='name']/text()",
            'default': "",
        },
        'url_name': {
            'method': '__getattribute__',
            'params': 'url',
            'process': 'process_url_name',
            'default': "",
        },
        'bio': {
            'method': 'xpath',
            'params': "//span[@class='bio']/text()",
            'default': "",
        },
        'business': {
            'method': 'xpath',
            'params': "//span[contains(@class,'business')]/a/text()",
            'default': "",
        },
        'business_topic_url': {
            'method': 'xpath',
            'params': "//span[contains(@class,'business')]/a/@href",
            'process': "process_selector_extract",
            'default': "",
        },
        'gender': {
            'method': 'xpath',
            'params': "//span[contains(@class,'gender')]/i/@class",
            'default': "",
        },
        'description': {
            'method': 'xpath',
            'params': "//span[contains(@class,'description')]//span//text()",
            'default': "",
        },
        'weibo_url': {
            'method': 'xpath',
            'params': "//div[@class='weibo-wrap']/a/@href",
            'process': "process_selector_extract",
            'default': "",
        },
        'followee_count': {
            'method': 'xpath',
            'params': "//div[@class='zm-profile-side-following zg-clear']/a[1]/strong/text()",
            'default': 0,
        },
        'follower_count': {
            'method': 'xpath',
            'params': "//div[@class='zm-profile-side-following zg-clear']/a[2]/strong/text()",
            'default': 0,
        },
        'questions_count': {
            'method': 'xpath',
            'params': "//div[@class='profile-navbar clearfix']/a[2]/span/text()",
            'process': 'process_questions_count',
            'default': 0,
        },
        'answers_count': {
            'method': 'xpath',
            'params': "//div[@class='profile-navbar clearfix']/a[3]/span/text()",
            'default': 0,
        },
        'posts_count': {
            'method': 'xpath',
            'params': "//div[@class='profile-navbar clearfix']/a[4]/span/text()",
            'default': 0,
        },
        'collections_count': {
            'method': 'xpath',
            'params': "//div[@class='profile-navbar clearfix']/a[5]/span/text()",
            'default': 0,
        },
        'logs_count': {
            'method': 'xpath',
            'params': "//div[@class='profile-navbar clearfix']/a[6]/span/text()",
            'default': 0,
        },
        'personal_page_view_count': {
            'method': 'xpath',
            'params': "//div[@class='zm-profile-side-section']/div[@class='zm-side-section-inner']/span/strong/text()",
            'default': 0,
        },
        'follow_columns_count': {
            'method': 'xpath',
            'params': "//a[contains(@href,'/columns/followed')]/strong/text()",
            'default': 0,
        },
        'follow_topics_count': {
            'method': 'xpath',
            'params': "//a[contains(@href,'/topics')]/strong/text()",
            'default': 0,
        },
    }