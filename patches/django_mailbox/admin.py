#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model configuration in application ``django_mailbox`` for administration
console.
"""

import logging

from django.conf import settings
from django.contrib import admin

from django_mailbox.models import MessageAttachment, Message, Mailbox
from django_mailbox.signals import message_received
from django_mailbox.utils import convert_header_to_unicode


logger = logging.getLogger(__name__)


def get_new_mail(mailbox_admin, request, queryset):
    for mailbox in queryset.all():
        logger.debug('Receiving mail for %s' % mailbox)
        mailbox.get_new_mail()
get_new_mail.short_description = 'Get new mail'


def resend_message_received_signal(message_admin, request, queryset):
    for message in queryset.all():
        logger.debug('Resending \'message_received\' signal for %s' % message)
        message_received.send(sender=message_admin, message=message)


resend_message_received_signal.short_description = (
    'Re-send message received signal'
)


def set_as_unprocessed(message_admin, request, queryset):
    queryset.update(processed_batch_apps=False)
set_as_unprocessed.short_description = 'Set as unprocessed by BA'


def set_as_processed(message_admin, request, queryset):
    queryset.update(processed_batch_apps=True)
set_as_processed.short_description = 'Set as processed by BA'


def strip_body(message_admin, request, queryset):
    queryset.update(encoded=False)
    queryset.update(body='')
strip_body.short_description = 'Strip message body'


class MailboxAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'uri',
        'from_email',
        'active',
    )
    actions = [get_new_mail]


class MessageAttachmentAdmin(admin.ModelAdmin):
    raw_id_fields = ('message', )
    list_display = ('message', 'document',)


class MessageAttachmentInline(admin.TabularInline):
    model = MessageAttachment
    extra = 0


class MessageAdmin(admin.ModelAdmin):

    def attachment_count(self, msg):
        return msg.attachments.count()

    def subject(self, msg):
        return convert_header_to_unicode(msg.subject)

    def sent_time(self, msg):
        return msg.sent_time

    inlines = [
        MessageAttachmentInline,
    ]
    list_display = (
        'subject',
        'matched_batch_apps',
        'processed_batch_apps',
        'sent_time',
        'processed',
        'read',
        'mailbox',
        'outgoing',
        'attachment_count',
    )
    ordering = ['-processed']
    list_filter = (
        'mailbox',
        'outgoing',
        'processed',
        'read',
    )
    exclude = (
        'body',
    )
    raw_id_fields = (
        'in_reply_to',
    )
    readonly_fields = (
        'text',
        'html',
    )
    actions = [resend_message_received_signal, set_as_unprocessed, set_as_processed, strip_body]

if getattr(settings, 'DJANGO_MAILBOX_ADMIN_ENABLED', True):
    admin.site.register(Message, MessageAdmin)
    admin.site.register(MessageAttachment, MessageAttachmentAdmin)
    admin.site.register(Mailbox, MailboxAdmin)
