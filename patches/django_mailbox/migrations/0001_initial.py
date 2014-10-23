# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mailbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('uri', models.CharField(default=None, blank=True, max_length=255, null=True, help_text="Example: imap+ssl://myusername:mypassword@someserver <br /><br />Internet transports include 'imap' and 'pop3'; common local file transports include 'maildir', 'mbox', and less commonly 'babyl', 'mh', and 'mmdf'. <br /><br />Be sure to urlencode your username and password should they contain illegal characters (like @, :, etc).", verbose_name='URI')),
                ('from_email', models.CharField(default=None, blank=True, max_length=255, null=True, help_text="Example: MailBot &lt;mailbot@yourdomain.com&gt;<br />'From' header to set for outgoing email.<br /><br />If you do not use this e-mail inbox for outgoing mail, this setting is unnecessary.<br />If you send e-mail without setting this, your 'From' header will'be set to match the setting `DEFAULT_FROM_EMAIL`.", verbose_name='From email')),
                ('active', models.BooleanField(default=True, verbose_name='Active', help_text='Check this e-mail inbox for new e-mail messages during polling cycles.  This checkbox does not have an effect upon whether mail is collected here when this mailbox receives mail from a pipe, and does not affect whether e-mail messages can be dispatched from this mailbox. ')),
            ],
            options={
                'verbose_name_plural': 'Mailboxes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(verbose_name='Subject', max_length=255)),
                ('message_id', models.CharField(verbose_name='Message ID', max_length=255)),
                ('sent_time', models.CharField(verbose_name='Sent Time', max_length=255)),
                ('from_header', models.CharField(verbose_name='From header', max_length=255)),
                ('to_header', models.TextField(verbose_name='To header')),
                ('outgoing', models.BooleanField(default=False, verbose_name='Outgoing')),
                ('body', models.TextField(verbose_name='Body')),
                ('encoded', models.BooleanField(default=False, verbose_name='Encoded', help_text='True if the e-mail body is Base64 encoded')),
                ('processed', models.DateTimeField(verbose_name='Processed', auto_now_add=True)),
                ('read', models.DateTimeField(default=None, verbose_name='Read', blank=True, null=True)),
                ('in_reply_to', models.ForeignKey(blank=True, null=True, to='django_mailbox.Message', related_name='replies', verbose_name='In reply to')),
                ('mailbox', models.ForeignKey(related_name='messages', to='django_mailbox.Mailbox', verbose_name='Mailbox')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headers', models.TextField(verbose_name='Headers', blank=True, null=True)),
                ('document', models.FileField(verbose_name='Document', upload_to='mailbox_attachments/%Y/%m/%d/')),
                ('message', models.ForeignKey(blank=True, null=True, to='django_mailbox.Message', related_name='attachments', verbose_name='Message')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
