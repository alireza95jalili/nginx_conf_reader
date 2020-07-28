import main
import argparse
import time

parser = argparse.ArgumentParser(
    description="Nginx Config CLI By AlirezaJalili.ir")
server = parser.add_argument_group()
upstream = parser.add_argument_group()


parser.add_argument(
    "-d", "--domain", help="Domain Name with ir/com/etc", metavar=("‌"),
)
parser.add_argument(
    "-b", "--block", help="upstream or Server block", metavar=("‌"),
)

parser.add_argument(
    "-p", "--prev_value", help="Previus Value That Want To Be Changed", metavar=("‌"),
)

parser.add_argument(
    "-n", "--new_value", help="New Value set on Prev_value", metavar=("‌"),
)

server.add_argument(
    "-r", "--directive", help="Directive of block", metavar=("‌"),
)

server.add_argument(
    "-a", "--attribute", help="Domain Name with ir/com/etc", metavar=("‌"),
)

parser.add_argument("-v", "--verbose", help="Show Every thing", metavar=("‌"))
parser.add_argument("--new_subdomain",
                    help="Add New Upstream Block", metavar=("‌"))
parser.add_argument("--ssl", help="Add New Upstream Block",
                    type=bool, metavar=("‌"))

args = parser.parse_args()
params = {
    "domain": args.domain,
    "block": args.block,
    "prev_value": args.prev_value,
    "new_value": args.new_value,
    "directive": args.directive,
    "attribute": args.attribute,
    "config": f"/etc/nginx/conf.d/{args.domain}.conf",
}
start_time = time.time()
main.bootstrap()
if not args.block:
    exit("Block Argu is not passed")
if not args.domain:
    exit("domain Argu is not passed")
if not args.prev_value:
    exit("prev_value Argu is not passed")
if not args.new_value:
    exit("new_value Argu is not passed")
if not args.directive and args.block == "server":
    exit("directive Argu is not passed")
if not args.attribute and args.block == "server":
    exit("attribute Argu is not passed")

if not args.new_subdomain:
    if args.block.lower() == "server":
        main.change_nginx_config(
            domain=str(args.domain),
            block_type="server",
            prev_value=args.prev_value,
            new_value=args.new_value,
            directive=args.directive,
            attribute=args.attribute,
        )
    elif args.block.lower() == "upstream":
        main.change_nginx_config(
            domain=args.domain,
            block_type="upstream",
            prev_value=args.prev_value,
            new_value=args.new_value,
            attribute=args.attribute,
        )
        main.log("Total Execution Time: {:.4f} Secounds :)".format(
            time.time() - start_time), "info")

    else:
        exit("cant Identify Block Name")
else:
    main.add_subdomain(domain=args.domain, sub_name=args.new_subdomain,)

# answer = args.square**2
# if args.verbose:
#     print("the square of {} equals {}".format(args.square, answer))
# else:
#     print(answer)
