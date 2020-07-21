from reserver import Reserver
from params import parse_argument

args = parse_argument()

reserver = Reserver(args=args)

if args.reserve:
    reserver.reserve_seat()
if args.update:
    reserver.check_list()
if args.cancel:
    reserver.cancel_reserve(args.cancel)
if args.qrcode:
    reserver.create_ticket()
