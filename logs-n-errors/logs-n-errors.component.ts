import { Component } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';

export interface PeriodicElement {
  position: number;
  userid: string;
  transactionState: string[];
  transactionId: string;
}

// let data: JSON;

const apiData = [
  {
    TransactionId: '61883b96-84ae-11ec-882a-0a0f0d3e0000',
    UserId: 'jbrown829@verizon.net',
    TransactionDetails: [
      {
        TransactionState: 'START',
        Type: 'INFO',
        ApigeeTransactionId: 'b8cbe26f-3a46-10a2-11dc-a199c7607fab',
        ServerInfo: 'DGLWEBPND02_DGLWEBIS01',
        CorrelationId: '61883b96-84ae-11ec-882a-0a0f0d3e0000',
        UiTransactionId: 'WEB_v3.0_4750c577-58bd-4739-98d8-ee220cdbc3c6',
        Date: '2022-02-03 00:01:43.714 EST',
        Thread: '38',
        TransactionId: '61883b96-84ae-11ec-882a-0a0f0d3e0000',
      },
      {
        TransactionState: 'INPROGRESS',
        Type: 'INFO',
        ApigeeTransactionId: 'b8cbe26f-3a46-10a2-11dc-a199c7607fab',
        ServerInfo: 'DGLWEBPND02_DGLWEBIS01',
        CorrelationId: '61883b96-84ae-11ec-882a-0a0f0d3e0000',
        UiTransactionId: 'WEB_v3.0_4750c577-58bd-4739-98d8-ee220cdbc3c6',
        Date: '2022-02-03 00:01:43.911 EST',
        Thread: '38',
        TransactionId: '61883b96-84ae-11ec-882a-0a0f0d3e0000',
      },
      {
        TransactionState: 'ERROR',
        Type: 'ERROR',
        ApigeeTransactionId: 'b8cbe26f-3a46-10a2-11dc-a199c7607fab',
        ServerInfo: 'DGLWEBPND02_DGLWEBIS01',
        CorrelationId: '61883b96-84ae-11ec-882a-0a0f0d3e0000',
        UiTransactionId: 'WEB_v3.0_4750c577-58bd-4739-98d8-ee220cdbc3c6',
        Date: '2022-02-03 00:01:44.005 EST',
        Thread: '38',
        TransactionId: '61883b96-84ae-11ec-882a-0a0f0d3e0000',
      },
    ],
  },

  {
    TransactionId: '0a06243e-7dfe-11ec-bc07-0a0f0d3e0000',
    UserId: 'Sanjai',
    TransactionDetails: [
      {
        TransactionState: 'START',
        TransactionTime: '2022-01-25T11:44:18.525 EST',
        Type: 'INFO',
        Log: 'com.bcbsma.web.api.getclaimdetailsservice.getclaimdetails - USER ID - sanjai\n',
        ApigeeTransactionId: '135c5349-e3d1-8a3e-b881-e10c7c18412e',
        ServerInfo: 'sameplservr',
        CorrelationId: '0a06243e-7dfe-11ec-bc07-0a0f0d3e0000',
        UiTransactionId: '5f3bf8e2-33d3-46f4-8deb-8acf1ce058f8',
        Date: '2022-01-25 11:44:18.525 EST',
        Thread: '87',
        TransactionId: '0a06243e-7dfe-11ec-bc07-0a0f0d3e0000',
      },
      {
        TransactionState: 'INPROGRESS',
        TransactionTime: '2022-01-25T11:44:35.780 EST',
        Type: 'INFO',
        Log: 'com.bcbsma.web.api - USER ID - sanjai\n',
        ApigeeTransactionId: '',
        ServerInfo: 'sameplservr',
        CorrelationId: '144ee98a-7dfe-11ec-bc07-0a0f0d3e0000',
        UiTransactionId: 'WEB_v3.0_41cc3b95-02e3-4d1c-8908-8d3ec2c68ec1',
        Date: '2022-01-25 11:44:35.780 EST',
        Thread: '234',
        TransactionId: '144ee98a-7dfe-11ec-bc07-0a0f0d3e0000',
      },
      {
        TransactionState: 'COMPLETED',
        TransactionTime: '2022-01-25T11:44:35.780 EST',
        Type: 'INFO',
        Log: 'com.bcbsma.web.api - USER ID - sanjai\n',
        ApigeeTransactionId: '',
        ServerInfo: 'sameplservr',
        CorrelationId: '144ee98a-7dfe-11ec-bc07-0a0f0d3e0000',
        UiTransactionId: 'WEB_v3.0_41cc3b95-02e3-4d1c-8908-8d3ec2c68ec1',
        Date: '2022-01-25 11:44:35.780 EST',
        Thread: '234',
        TransactionId: '144ee98a-7dfe-11ec-bc07-0a0f0d3e0000',
      },
    ],
  },

  {
    TransactionId: '0a06243e-7dfe-11ec-bc07-0a0f0d3e0000',
    UserId: 'Sanjai',
    TransactionDetails: [
      {
        TransactionState: 'START',
        TransactionTime: '2022-01-25T11:44:18.525 EST',
        Type: 'INFO',
        Log: 'com.bcbsma.web.api.getclaimdetailsservice.getclaimdetails - USER ID - sanjai\n',
        ApigeeTransactionId: '135c5349-e3d1-8a3e-b881-e10c7c18412e',
        ServerInfo: 'sameplservr',
        CorrelationId: '0a06243e-7dfe-11ec-bc07-0a0f0d3e0000',
        UiTransactionId: '5f3bf8e2-33d3-46f4-8deb-8acf1ce058f8',
        Date: '2022-01-25 11:44:18.525 EST',
        Thread: '87',
        TransactionId: '0a06243e-7dfe-11ec-bc07-0a0f0d3e0000',
      },
      {
        TransactionState: 'INPROGRESS',
        TransactionTime: '2022-01-25T11:44:35.780 EST',
        Type: 'INFO',
        Log: 'com.bcbsma.web.api - USER ID - sanjai\n',
        ApigeeTransactionId: '',
        ServerInfo: 'sameplservr',
        CorrelationId: '144ee98a-7dfe-11ec-bc07-0a0f0d3e0000',
        UiTransactionId: 'WEB_v3.0_41cc3b95-02e3-4d1c-8908-8d3ec2c68ec1',
        Date: '2022-01-25 11:44:35.780 EST',
        Thread: '234',
        TransactionId: '144ee98a-7dfe-11ec-bc07-0a0f0d3e0000',
      },
      {
        TransactionState: 'ERROR',
        TransactionTime: '2022-01-25T11:44:35.780 EST',
        Type: 'INFO',
        Log: 'com.bcbsma.web.api - USER ID - sanjai\n',
        ApigeeTransactionId: '',
        ServerInfo: 'sameplservr',
        CorrelationId: '144ee98a-7dfe-11ec-bc07-0a0f0d3e0000',
        UiTransactionId: 'WEB_v3.0_41cc3b95-02e3-4d1c-8908-8d3ec2c68ec1',
        Date: '2022-01-25 11:44:35.780 EST',
        Thread: '234',
        TransactionId: '144ee98a-7dfe-11ec-bc07-0a0f0d3e0000',
      },
    ],
  },
];

// let element_data = function () {
//   let returnElementData: PeriodicElement[] = [];
//   for (let dataItem of apiData) {
//     let tempArr = [];
//     for (let itemDetail of dataItem.TransactionDetails) {
//       tempArr.push(itemDetail.TransactionState);
//     }
//     returnElementData.push({
//       position: 1,
//       userid: dataItem.UserId,
//       transactionState: tempArr,
//       transactionId: dataItem.TransactionId,
//     });
//   }
//   return returnElementData;
// };

function populatingElementData() {
  let returnElementData: PeriodicElement[] = [];
  for (let dataItem of apiData) {
    let tempArr = [];
    for (let itemDetail of dataItem.TransactionDetails) {
      tempArr.push(itemDetail.TransactionState);
    }
    returnElementData.push({
      position: 1,
      userid: dataItem.UserId,
      transactionState: tempArr,
      transactionId: dataItem.TransactionId,
    });
  }
  return returnElementData;
}

const FINAL_ELEMENT: PeriodicElement[] = populatingElementData();

console.log(FINAL_ELEMENT);

// [
//   {
//     position: 1,
//     userid: apiData[0].UserId,
//     transactionState: [
//       apiData[0].TransactionDetails[0].TransactionState,
//       apiData[0].TransactionDetails[1].TransactionState,
//       apiData[0].TransactionDetails[2].TransactionState,
//     ],
//     transactionId: apiData[0].TransactionId,
//   },
//   {
//     position: 2,
//     userid: apiData[1].UserId,
//     transactionState: [
//       apiData[1].TransactionDetails[0].TransactionState,
//       apiData[0].TransactionDetails[1].TransactionState,
//       apiData[0].TransactionDetails[2].TransactionState,
//     ],
//     transactionId: apiData[1].TransactionId,
//   },
// ];

// [
//   {
//     position: 1,
//     userid: 'Hydrogen',
//     transactionState: 1.0079,
//     transactionId: 'H',
//   },
//   {
//     position: 2,
//     userid: 'Helium',
//     transactionState: 4.0026,
//     transactionId: 'He',
//   },
//   {
//     position: 3,
//     userid: 'Lithium',
//     transactionState: 6.941,
//     transactionId: 'Li',
//   },
//   {
//     position: 4,
//     userid: 'Beryllium',
//     transactionState: 9.0122,
//     transactionId: 'Be',
//   },
//   {
//     position: 5,
//     userid: 'Boron',
//     transactionState: 10.811,
//     transactionId: 'B',
//   },
//   {
//     position: 6,
//     userid: 'Carbon',
//     transactionState: 12.0107,
//     transactionId: 'C',
//   },
//   {
//     position: 7,
//     userid: 'Nitrogen',
//     transactionState: 14.0067,
//     transactionId: 'N',
//   },
//   {
//     position: 8,
//     userid: 'Oxygen',
//     transactionState: 15.9994,
//     transactionId: 'O',
//   },
//   {
//     position: 9,
//     userid: 'Fluorine',
//     transactionState: 18.9984,
//     transactionId: 'F',
//   },
//   {
//     position: 10,
//     userid: 'Neon',
//     transactionState: 20.1797,
//     transactionId: 'Ne',
//   },
// ];

/**
 * @title Table with filtering
 */
@Component({
  selector: 'app-logs-n-errors',
  templateUrl: './logs-n-errors.component.html',
  styleUrls: ['./logs-n-errors.component.css'],
})
export class LogsNErrorsComponent {
  displayedColumns: string[] = [
    'position',
    'userid',
    'transactionState',
    'transactionId',
  ];
  dataSource = new MatTableDataSource(FINAL_ELEMENT);

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }
}

///////////////////////////////////////////////////////////////////////////

// import { AfterViewInit, Component, ViewChild } from '@angular/core';
// import { MatPaginator } from '@angular/material/paginator';
// import { MatSort } from '@angular/material/sort';
// import { MatTableDataSource } from '@angular/material/table';

// export interface UserData {
//   id: string;
//   name: string;
//   progress: string;
//   fruit: string;
// }

// /** Constants used to fill up our data base. */
// const FRUITS: string[] = [
//   'blueberry',
//   'lychee',
//   'kiwi',
//   'mango',
//   'peach',
//   'lime',
//   'pomegranate',
//   'pineapple',
// ];
// const NAMES: string[] = [
//   'Maia',
//   'Asher',
//   'Olivia',
//   'Atticus',
//   'Amelia',
//   'Jack',
//   'Charlotte',
//   'Theodore',
//   'Isla',
//   'Oliver',
//   'Isabella',
//   'Jasper',
//   'Cora',
//   'Levi',
//   'Violet',
//   'Arthur',
//   'Mia',
//   'Thomas',
//   'Elizabeth',
// ];

// /**
//  * @title Data table with sorting, pagination, and filtering.
//  */
// @Component({
//   selector: 'app-logs-n-errors',
//   templateUrl: './logs-n-errors.component.html',
//   styleUrls: ['./logs-n-errors.component.css'],
// })
// export class LogsNErrorsComponent implements AfterViewInit {
//   displayedColumns: string[] = ['id', 'name', 'progress', 'fruit'];
//   dataSource: MatTableDataSource<UserData>;

//   @ViewChild(MatPaginator) paginator: MatPaginator;
//   @ViewChild(MatSort) sort: MatSort;

//   constructor() {
//     // Create 100 users
//     const users = Array.from({ length: 100 }, (_, k) => createNewUser(k + 1));

//     // Assign the data to the data source for the table to render
//     this.dataSource = new MatTableDataSource(users);
//   }

//   ngAfterViewInit() {
//     this.dataSource.paginator = this.paginator;
//     this.dataSource.sort = this.sort;
//   }

//   applyFilter(event: Event) {
//     const filterValue = (event.target as HTMLInputElement).value;
//     this.dataSource.filter = filterValue.trim().toLowerCase();

//     if (this.dataSource.paginator) {
//       this.dataSource.paginator.firstPage();
//     }
//   }
// }

// /** Builds and returns a new User. */
// function createNewUser(id: number): UserData {
//   const name =
//     NAMES[Math.round(Math.random() * (NAMES.length - 1))] +
//     ' ' +
//     NAMES[Math.round(Math.random() * (NAMES.length - 1))].charAt(0) +
//     '.';

//   return {
//     id: id.toString(),
//     name: name,
//     progress: Math.round(Math.random() * 100).toString(),
//     fruit: FRUITS[Math.round(Math.random() * (FRUITS.length - 1))],
//   };
// }

//////////////////////////////////////////////////////////////////////

// import { Component, OnInit } from '@angular/core';

// @Component({
//   selector: 'app-logs-n-errors',
//   templateUrl: './logs-n-errors.component.html',
//   styleUrls: ['./logs-n-errors.component.css']
// })
// export class LogsNErrorsComponent implements OnInit {

//   constructor() { }

//   ngOnInit(): void {
//   }

// }
