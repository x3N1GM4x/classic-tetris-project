from .command import Command, CommandException, register_command
from ..util import Platform

@register_command("pb", "getpb")
class GetPBCommand(Command):
    usage = "pb [username] (default username you)"

    def execute(self, username=None):
        if self.context.platform == Platform.DISCORD:
            platform_user = (Command.discord_user_from_username(username) if username
                             else self.context.platform_user)
        elif self.context.platform == Platform.TWITCH:
            platform_user = (Command.twitch_user_from_username(username) if username
                             else self.context.platform_user)

        if not platform_user:
            self.send_message("User has not set a PB.")
            return

        user = platform_user.user
        if user.ntsc_pb and user.pal_pb:
            self.send_message("{user_tag} has an NTSC PB of {ntsc:,} and a PAL PB of {pal:,}.".format(
                user_tag=platform_user.user_tag,
                ntsc=user.ntsc_pb,
                pal=user.pal_pb
            ))
        else:
            if user.ntsc_pb:
                self.send_message("{user_tag} has an NTSC PB of {ntsc:,}.".format(
                    user_tag=platform_user.user_tag,
                    ntsc=user.ntsc_pb
                ))
            elif user.pal_pb:
                self.send_message("{user_tag} has a PAL PB of {pb:,}.".format(
                    user_tag=platform_user.user_tag,
                    pb=user.pal_pb
                ))
            else:
                self.send_message("User has not set a PB.")



@register_command("newpb", "setpb")
class SetPBCommand(Command):
    usage = "setpb <pb> [type] (default type NTSC)"

    def execute(self, pb, pb_type="ntsc"):
        try:
            pb = int(pb.replace(",", ""))
        except ValueError:
            raise CommandException(send_usage=True)

        pb_type = pb_type.lower()

        if pb < 0:
            self.send_message("Invalid PB.")
        elif pb > 1400000:
            self.send_message("You wish, kid >.>")
        else:
            if self.context.user.set_pb(pb, pb_type):
                self.send_message("{user_tag} has a new {pb_type} pb of {pb:,}!".format(
                    user_tag=self.context.user_tag,
                    pb_type=pb_type.upper(),
                    pb=pb
                ))
            else:
                self.send_message("Invalid PB type - must be NTSC or PAL (default NTSC)")