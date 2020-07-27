import sh
import nginx
import subprocess
import logging
import os
from logging.handlers import SysLogHandler


def log(msg: str, lvl: str, extra=None):
    file_name = "[Nginx-Config-Main]"
    print(f"{file_name}: [{lvl}]\t {msg}")
    return True
    logger = logging.getLogger()
    logger.addHandler(SysLogHandler("/dev/log"))
    logger.addHandler(logging.FileHandler("nginx-main.log"))

    lvl = lvl.upper()

    if lvl == "NOTSET":
        pass
        # logger.info(f"{file_name}: [{lvl}]\t {msg}")

    elif lvl == "DEBUG":
        logger.debug(f"{file_name}: [{lvl}]\t {msg}")

    elif lvl == "INFO":
        logger.info(f"{file_name}: [{lvl}]\t {msg}")

    elif lvl == "WARNING":
        logger.warning(f"{file_name}: [{lvl}]\t {msg}")

    elif lvl == "ERROR":
        logger.error(f"{file_name}: [{lvl}]\t {msg}")

    elif lvl == "CRITICAL":
        logger.critical(f"{file_name}: [{lvl}]\t {msg}")

    else:
        logger.error("Not Working")


def bootstrap():

    try:
        os.mkdir("/etc/nginx/alirezajalili.ir.d/")
        log.debug("Folder Created!")
    except FileExistsError:
        pass
    except Exception as error:
        log(error, "error")
    else:
        return True

    try:
        os.mkdir("/etc/nginx/alirezajalili.ir.d/in_conf.d")
        log.debug("Folder Created!")
    except FileExistsError:
        pass
    except Exception as error:
        log(error, "error")
    else:
        return True

    try:
        os.mkdir("/etc/nginx/alirezajalili.ir.d/out.conf.d")
        log.debug("Folder Created!")
    except FileExistsError:
        pass
    except Exception as error:
        log(error, "error")
    else:
        return True

    try:
        os.mkdir("/etc/nginx/alirezajalili.ir.d/json_conf.d")
        log.debug("Folder Created!")
    except FileExistsError:
        pass
    except Exception as error:
        log(error, "error")
    else:
        return True


json_config_dir = "/etc/nginx/alirezajalili.ir.d/json_conf.d"
in_config_dir = "/etc/nginx/alirezajalili.ir.d/in_conf.d"
config_tmp_dir = "/etc/nginx/alirezajalili.ir.d/out.conf.d"
cnfm = nginx.conf_manipulator()


def change_nginx_config(
    domain: str,
    block_type: str,
    prev_value: list,
    new_value: list,
    directive=None,
    attribute=None,
):
    config_dir = f"/etc/nginx/conf.d/{domain}.conf"
    os.system(f"cp {config_dir} {in_config_dir}/{domain}.conf")
    config_dir = f"{in_config_dir}/{domain}.conf"
    try:
        addHttpBlock(config_dir)
    except Exception as error:
        log(error, "error", "\t in change_nginx_config -> add http block")
    else:
        # log("Http Block Added", "info")
        # return True

    try:
        cnfm.conf2json(
            config_dir, output_name=f"{json_config_dir}/{domain}.json")
    except Exception as error:
        log("Cant Read Site Config or Save New Json Config", "error")
        log(error, "error")
        log(config_dir, "info")
        print(f"cp {config_dir} {in_config_dir}/{domain}.conf")
        return False
    else:
        if block_type == "server":
            try:
                if directive == None or attribute == None:
                    log("Directive or Attribute is None", error)
                    return False
                cnfm.change_conf(
                    block="server",
                    prev_value=prev_value,
                    new_value=new_value,
                    directive=directive,
                    attribute=attribute,
                    jsonfile=f"{json_config_dir}/{domain}.json",
                )
            except Exception as error:
                log(error, "error")
                return False
            else:
                try:
                    cnfm.json2conf(
                        jsonfile=f"{json_config_dir}/{domain}.json",
                        dir=f"out.conf.d/{domain}.conf",
                    )
                except Exception as error:
                    log(error, "error")
                    return False
                else:
                    try:
                        os.remove(config_dir)
                    except Exception as error:
                        log("cant remove Old Config", "error")
                        log(error, "error")
                        return False
                    else:
                        try:
                            os.rename(
                                f"{config_dir}/{domain}.conf", config_dir)
                        except Exception as error:
                            log("cant move new config to site-avilable", error)
                            log(error, "error")
                            return False
                        else:
                            return True

        elif block_type == "upstream":
            try:
                cnfm.change_conf(
                    block="upstream",
                    prev_value=prev_value,
                    new_value=new_value,
                    jsonfile=f"{json_config_dir}/{domain}.json",
                )
            except Exception as error:
                log(error, "error", "173")
            else:
                try:
                    cnfm.json2conf(
                        jsonfile=f"{json_config_dir}/{domain}.json",
                        dir=f"{config_tmp_dir}/{config_dir}",
                    )
                except Exception as error:
                    log("Cant Save New Config.", "error")
                    log(error, "error")
                    return False
                else:
                    try:
                        # os.remove(config_dir)
                        pass
                    except Exception as error:
                        log("Cant remove Old Config", "error")
                        log(error, "error")
                        return False
                    else:
                        try:
                            log(config_dir, "debug")
                            log(config_tmp_dir, "debug")
                            os.rename(
                                config_dir, f"{config_tmp_dir}/{domain}.conf")
                        except Exception as error:
                            log("cant move new config to site-avilable", "error")
                            log(error, "error")
                            return False
                        else:
                            new_file = f"{config_tmp_dir}/{domain}.conf"
                            deleteHttpBlock(new_file)
                            return True
        else:
            log("Cant Identify Block Type", "Error")
            return False


def add_subdomain(domain=str, sub_name=str, ssl=bool):
    try:
        cnfm.add_subdomain(domain=str, sub_name=str, ssl=bool)
    except:
        print("cant add new sub domain")
        return False
    else:
        return True


def delete_catch(domain: str, sub: str, all=bool):
    if not sub:
        try:
            os.removedirs(f"/etc/nginx/cache/{domain}")
        except:
            return False
    elif sub and not all:
        try:
            os.removedirs(f"/etc/nginx/cache/{sub}.{domain}")
        except:
            return False
    elif sub and all:
        try:
            os.removedirs(f"/etc/nginx/cache/{domain}")
            os.removedirs(f"/etc/nginx/cache/{sub}.{domain}")
        except:
            return False


def dev_mode(domain: str, status=bool):
    config_dir = f"/etc/nginx/conf.d/{domain}"
    try:
        cnfm.conf2json(
            nginx_config=config_dir, output_name=f"/out.conf.d/aj/json/{domain}.json"
        )
        config = cnfm.dev_mod(
            config_dir=f"/out.conf.d/aj/json/{domain}.json", status=status
        )
        cnfm.json2conf(jsonfile=config, dir="/etc/nginx/conf.d")
    except Exception:
        print("ERROR: Cant change catch Mode")
    else:
        return True


def addHttpBlock(filename: str):
    # os.system("sed -i '1s/^/http { #HTTPBLOCK\n/' alirezajalili.ir.conf")
    # sed -i '1s/\(.*\)/insertedtext\n\1/' /etc/nginx/alirezajalili.ir.d/in_conf.d/alirezajalili.ir.conf
    try:
        with open(f"{filename}", "r+") as f:
            lines = f.readlines()
            f.seek(0)
            f.write("http { #HTTPBLOCK\n")
            for line in lines:  # write old content after new
                f.write(line)

        os.system("""echo '} #HTTPBLOCK' >> %s""" % filename)
    except Exception as error:
        print(error)
        log(error, error, "Block = Httpblock")

    # output = subprocess.run(["sed", "-i", '1s/\(.*\)/http { #HTTPBLOCK\n\1/', f'{}'])


def deleteHttpBlock(filename: str):
    try:
        with open(f"{filename}", "r") as f:
            lines = f.readlines()
        with open(f"{filename}", "w") as f:
            for line in lines:
                if not line.strip("\n").__contains__("#HTTPBLOCK"):
                    f.write(line)
                else:
                    print(line)
    except Exception as e:
        log(e, "error")
    else:
        # log("HTTP Block Rrmoved", "info")
        return True
