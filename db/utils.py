# coding: utf-8

from .entity import Vm

from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    create_engine, 
    Table, 
    Column, 
    # Integer,
    String, 
    MetaData, 
    # ForeignKey
)


sqlURL = 'mysql://dra:cshuo@controller/machineDB'
engine = create_engine(sqlURL)


def create_vm_table():
    meta_data = MetaData()
    vm_table = Table(
            'vm', meta_data,
            Column('name', String(32), primary_key=True),
            Column('vm_type', String(32)),
            Column('host', String(32)),
    )
    meta_data.create_all(engine)


class DbUtil(object):
    def __init__(self):
        self.DBSession = sessionmaker(bind=engine)

    def add_vm(self, name, vm_type, host):
        session = self.DBSession()
        new_vm = Vm(name=name, vm_type=vm_type, host=host)
        try:
            session.add(new_vm)
            session.commit()
        except:
            session.close()
            return False
        session.close()
        return True

    def rm_vm(self, vm_name):
        """
        return True for delete vm successfully, or return False
        """
        session = self.DBSession()
        try:
            vm_inst = session.query(Vm).filter(Vm.name == vm_name).one()
        except:
            session.close()
            return False
        session.delete(vm_inst)
        session.commit()
        session.close()
        return True

    def query_vm(self, vm_name):
        """
        return dict of vm info, None for None
        :param vm_name: the name of the virtual machine
         :type vm_name: str[32]
        :return: the information of the virtual machine
         :rtype: dict(str: *)
        """
        session = self.DBSession()
        try:
            vm_inst = session.query(Vm).filter(Vm.name == vm_name).one()
        except:
            session.close()
            return None
        vm_info = dict()
        vm_info['name'] = vm_inst.name
        vm_info['type'] = vm_inst.vm_type
        vm_info['host'] = vm_inst.host
        session.close()
        return vm_info

    def modify_vm(self, vm_name, new_host):
        """ NOTE: for dra, the only changes for vm is the host info after
            the vm is migrated
        """
        session = self.DBSession()
        try:
            vm_inst = session.query(Vm).filter(Vm.name == vm_name).one()
        except:
            session.close()
            return False
        vm_inst.host = new_host
        session.commit()
        session.close()
        return True


if __name__ == '__main__':
    create_vm_table()
    db = DbUtil()
    if db.add_vm('test1', 'normal', 'compute1'):
        print "add ok"
    if db.rm_vm('test1'):
        print "rm ok"
    print db.query_vm('test1')
